import os
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp
from datetime import datetime, timedelta
import logging

from .models import Message, GmailSyncState, GmailMessage

User = get_user_model()
logger = logging.getLogger(__name__)


def parse_message_headers(headers_list):
    """Parse Gmail headers list into a dict."""
    return {h['name']: h['value'] for h in headers_list}


def extract_email_from_header(header_value):
    """Extract email from 'Name <email@example.com>' format."""
    if not header_value:
        return ''
    # Simple extraction - could be improved with email.utils.parseaddr
    if '<' in header_value and '>' in header_value:
        return header_value.split('<')[1].split('>')[0]
    return header_value


def determine_direction(label_ids):
    """Determine if message is inbox or sent."""
    return 'sent' if 'SENT' in label_ids else 'inbox'


def has_attachments(payload):
    """Check if message has attachments."""
    if not payload:
        return False

    # Check parts for attachments
    parts = payload.get('parts', [])
    for part in parts:
        if part.get('filename'):
            return True
        # Check nested parts
        if part.get('parts'):
            for nested_part in part['parts']:
                if nested_part.get('filename'):
                    return True
    return False


def is_message_read(label_ids):
    """Check if message is read (doesn't have UNREAD label)."""
    return 'UNREAD' not in label_ids


@shared_task
def ping():
    return f"pong at {timezone.now().isoformat()}"


def get_gmail_service(user):
    """
    Get authenticated Gmail API service for a user.
    Uses OAuth tokens from django-allauth.
    """
    try:
        # Get the Google social account for this user
        social_token = SocialToken.objects.filter(
            account__user=user,
            account__provider='google'
        ).first()

        if not social_token:
            logger.error(f"No Google OAuth token found for user {user.id}")
            return None

        # Create credentials object
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

        
        creds = Credentials(
            token=social_token.token,
            refresh_token=social_token.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
        )

        # Build Gmail API service
        service = build('gmail', 'v1', credentials=creds)
        return service

    except Exception as e:
        logger.error(f"Error creating Gmail service for user {user.id}: {e}")
        return None


@shared_task
def sync_gmail_metadata(user_id, days=7):
    """
    Sync Gmail messages for a user.

    Args:
        user_id: User ID to sync emails for
        days: Number of days of history to fetch (default: 7)
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Starting Gmail sync for user {user.username} (last {days} days)")

        # Get Gmail API service
        service = get_gmail_service(user)
        if not service:
            logger.error(f"Could not create Gmail service for user {user.id}")
            return {"error": "Could not authenticate with Gmail"}

        # Calculate date range
        after_date = datetime.now() - timedelta(days=days)
        after_timestamp = int(after_date.timestamp())

        # Fetch message list
        query = f"after:{after_timestamp}"
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=500  # Adjust as needed
        ).execute()

        messages = results.get('messages', [])
        logger.info(f"Found {len(messages)} messages for user {user.username}")

        synced_count = 0
        for msg in messages:
            msg_id = msg['id']

            # Check if we already have this message
            if Message.objects.filter(gmail_id=msg_id, owner=user).exists():
                continue

            # Fetch full message details
            full_msg = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()

            # Parse headers
            headers = {h['name']: h['value'] for h in full_msg['payload'].get('headers', [])}

            # Determine direction (inbox vs sent)
            label_ids = full_msg.get('labelIds', [])
            direction = 'sent' if 'SENT' in label_ids else 'inbox'

            # Create Message object
            Message.objects.create(
                owner=user,
                gmail_id=msg_id,
                thread_id=full_msg.get('threadId', ''),
                internal_date=datetime.fromtimestamp(int(full_msg['internalDate']) / 1000),
                from_email=headers.get('From', ''),
                to_email=headers.get('To', ''),
                subject=headers.get('Subject', ''),
                label_ids=label_ids,
                direction=direction,
                snippet=full_msg.get('snippet', '')
            )
            synced_count += 1

        # Update sync state
        sync_state, created = GmailSyncState.objects.get_or_create(owner=user)
        sync_state.last_history_id = results.get('historyId', '')
        sync_state.save()

        logger.info(f"Successfully synced {synced_count} new messages for user {user.username}")
        return {
            "success": True,
            "user_id": user_id,
            "synced_count": synced_count,
            "total_found": len(messages)
        }

    except User.DoesNotExist:
        logger.error(f"User {user_id} does not exist")
        return {"error": f"User {user_id} not found"}
    except Exception as e:
        logger.error(f"Error syncing Gmail for user {user_id}: {e}")
        return {"error": str(e)}