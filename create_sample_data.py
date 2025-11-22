#!/usr/bin/env python
"""
Script to create sample DailyStat data for testing the API
Run with: python manage.py shell < create_sample_data.py
"""
from django.contrib.auth import get_user_model
from analytics.models import DailyStat
from datetime import date, timedelta
import random

User = get_user_model()

# Get or create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"Created user: {user.username}")
else:
    print(f"Using existing user: {user.username}")

# Create 14 days of sample data
print("Creating sample daily stats...")
for i in range(14):
    day = date.today() - timedelta(days=i)

    stat, created = DailyStat.objects.get_or_create(
        owner=user,
        date=day,
        defaults={
            'inbox_count': random.randint(20, 80),
            'sent_count': random.randint(10, 40),
            'work': random.randint(10, 30),
            'personal': random.randint(5, 25),
            'promotions': random.randint(5, 20),
        }
    )

    if created:
        print(f"  Created stats for {day}: {stat.inbox_count} inbox, {stat.sent_count} sent")
    else:
        print(f"  Stats for {day} already exist")

print("\nDone! You can now:")
print("1. Login with username: testuser, password: testpass123")
print("2. Visit: http://localhost:8000/api/analytics/daily-stats/")