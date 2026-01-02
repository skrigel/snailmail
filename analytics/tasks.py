from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import logging

from mail.models import Message
from .models import DailyStat

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task
def calculate_daily_stats(user_id, days=30):
    """
    Calculate daily email statistics for a user.
    Aggregates Message data into DailyStat records.

    Args:
        user_id: User ID to calculate stats for
        days: Number of days back to calculate (default: 30)
    """
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"Calculating daily stats for user {user.username} (last {days} days)")

        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        # Get messages in date range
        messages = Message.objects.filter(
            owner=user,
            internal_date__date__gte=start_date,
            internal_date__date__lte=end_date
        )

        # Group by date
        dates = messages.dates('internal_date', 'day')

        stats_created = 0
        stats_updated = 0

        for date in dates:
            # Get messages for this date
            day_messages = messages.filter(internal_date__date=date)

            # Count by direction
            inbox_count = day_messages.filter(direction='inbox').count()
            sent_count = day_messages.filter(direction='sent').count()

            # Count by category (from label_ids)
            work_count = day_messages.filter(label_ids__contains=['CATEGORY_WORK']).count()
            personal_count = day_messages.filter(label_ids__contains=['CATEGORY_PERSONAL']).count()
            promotions_count = day_messages.filter(label_ids__contains=['CATEGORY_PROMOTIONS']).count()

            # Create or update DailyStat
            stat, created = DailyStat.objects.update_or_create(
                owner=user,
                date=date,
                defaults={
                    'inbox_count': inbox_count,
                    'sent_count': sent_count,
                    'work': work_count,
                    'personal': personal_count,
                    'promotions': promotions_count,
                }
            )

            if created:
                stats_created += 1
            else:
                stats_updated += 1

        logger.info(
            f"Daily stats calculation complete for {user.username}: "
            f"{stats_created} created, {stats_updated} updated"
        )

        return {
            "success": True,
            "user_id": user_id,
            "stats_created": stats_created,
            "stats_updated": stats_updated,
            "date_range": f"{start_date} to {end_date}"
        }

    except User.DoesNotExist:
        logger.error(f"User {user_id} does not exist")
        return {"error": f"User {user_id} not found"}
    except Exception as e:
        logger.error(f"Error calculating daily stats for user {user_id}: {e}")
        return {"error": str(e)}