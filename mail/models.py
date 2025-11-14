from django.db import models
from django.contrib.auth import get_user_model

# https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.MessagePart
User = get_user_model()

# mail/models.py (assumed)
class GmailSyncState(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gmail_state")
    last_history_id = models.CharField(max_length=64, blank=True)


#Message Model From Google
# {
#   "id": string,
#   "threadId": string,
#   "labelIds": [
#     string
#   ],
#   "snippet": string,
#   "historyId": string,
#   "internalDate": string,
#   "payload": {
#     object (MessagePart)
#   },
#   "sizeEstimate": integer,
#   "raw": string
# }


## Message Part Model
# {
#   "partId": string,
#   "mimeType": string,
#   "filename": string,
#   "headers": [
#     {
#       object (Header)
#     }
#   ],
#   "body": {
#     object (MessagePartBody)
#   },
#   "parts": [
#     {
#       object (MessagePart)
#     }
#   ]
# }


## Header
# {
#   "name": string,
#   "value": string
# }

##message Part Body
# {
#   "attachmentId": string,
#   "size": integer,
#   "data": string
# }



class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gmail_id = models.CharField(max_length=128, unique=True)
    thread_id = models.CharField(max_length=128)
    internal_date = models.DateTimeField()           # Gmail internalDate -> DateTime
    from_email = models.EmailField(max_length=254, blank=True)
    to_email = models.EmailField(max_length=254, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    label_ids = models.JSONField(default=list)       # ['INBOX','CATEGORY_PERSONAL',...]
    direction = models.CharField(max_length=10)      # 'inbox' | 'sent'
    snippet = models.CharField(max_length=255, blank=True)  # short, harmless

    class Meta:
        indexes = [
            models.Index(fields=["owner","internal_date"]),
            models.Index(fields=["owner","direction"]),
        ]
        ordering = ["-internal_date"]