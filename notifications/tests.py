from django.test import TestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification
import notifications.signals  # ✅ Forces signal connection during test

User = get_user_model()

class NotificationTests(TestCase):
    def test_notification_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='pass123')
        self.assertTrue(Notification.objects.filter(recipient=user).exists())
