from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class GoogleUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=128, unique=True)
    
