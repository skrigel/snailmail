from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class DailyStat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    inbox_count = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    work = models.IntegerField(default=0)
    personal = models.IntegerField(default=0)
    promotions = models.IntegerField(default=0)

    class Meta:
        unique_together = ("owner","date")
        indexes = [models.Index(fields=["owner","date"])]