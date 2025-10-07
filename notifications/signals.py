from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Notification

@receiver(post_save, sender=CustomUser)
def notify_user_creation(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance,
            message=f"Welcome {instance.username}! Your account has been created."
        )
