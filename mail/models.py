from django.db import models
from django.contrib.auth import get_user_model

# https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.MessagePart
User = get_user_model()



class GmailSyncState(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gmail_state")
    last_history_id = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"GmailSyncState for {self.owner.username}"



### Full Gmail API Models ###
class GmailMessagePartBody(models.Model):
    """Represents the body of a Gmail message part."""
    attachment_id = models.CharField(max_length=128, blank=True)
    size = models.IntegerField(default=0)
    data = models.TextField(blank=True)

    def __str__(self):
        return f"Body (size={self.size})"


class GmailMessagePart(models.Model):
    """Represents a part of a Gmail message (can be nested)."""
    part_id = models.CharField(max_length=128, blank=True)
    mime_type = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    headers = models.JSONField(default=list)  # List of {"name": str, "value": str}
    body = models.ForeignKey(
        GmailMessagePartBody,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='message_parts'
    )
    parent_part = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='parts'
    )
    parent_message = models.ForeignKey(
        'GmailMessage',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='all_parts'
    )

    def __str__(self):
        return f"Part {self.part_id} ({self.mime_type})"


class GmailMessage(models.Model):
    """Full Gmail API message structure - mirrors the Gmail API response."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gmail_messages')
    gmail_id = models.CharField(max_length=128, unique=True)
    thread_id = models.CharField(max_length=128, db_index=True)
    label_ids = models.JSONField(default=list)
    snippet = models.CharField(max_length=255, blank=True)
    history_id = models.CharField(max_length=64, blank=True)
    internal_date = models.BigIntegerField()  # Unix timestamp in milliseconds
    payload = models.ForeignKey(
        GmailMessagePart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+'
    )
    size_estimate = models.IntegerField(default=0)
    raw = models.TextField(blank=True)  # Base64url encoded raw message

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-internal_date']
        indexes = [
            models.Index(fields=['owner', '-internal_date']),
            models.Index(fields=['thread_id']),
        ]

    def __str__(self):
        return f"Gmail Message {self.gmail_id}"


### Analytics Message ###
class Message(models.Model):
    """Simplified message model for email analytics and snail race dashboard."""

    DIRECTION_CHOICES = [
        ('inbox', 'Inbox'),
        ('sent', 'Sent'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    gmail_id = models.CharField(max_length=128, unique=True, db_index=True)
    thread_id = models.CharField(max_length=128, db_index=True)
    internal_date = models.DateTimeField(db_index=True)  # Converted from Gmail timestamp

    # Email metadata
    from_email = models.EmailField(max_length=254, blank=True)
    to_email = models.EmailField(max_length=254, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    snippet = models.CharField(max_length=255, blank=True)

    # Classification
    label_ids = models.JSONField(default=list)  # ['INBOX', 'CATEGORY_PERSONAL', 'SENT', ...]
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, db_index=True)

    # Analytics helpers
    has_attachment = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    # Reference to full Gmail message if needed
    gmail_message = models.OneToOneField(
        GmailMessage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analytics_message'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner', '-internal_date']),
            models.Index(fields=['owner', 'direction']),
            models.Index(fields=['owner', 'direction', '-internal_date']),
        ]
        ordering = ['-internal_date']

    def __str__(self):
        return f"{self.direction.upper()}: {self.subject[:50]}"

    @property
    def category(self):
        """Extract primary category from labels."""
        categories = [label for label in self.label_ids if label.startswith('CATEGORY_')]
        if categories:
            return categories[0].replace('CATEGORY_', '').lower()
        return 'uncategorized'
    