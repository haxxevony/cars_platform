from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        if instance.is_seller():
            SellerProfile = apps.get_model('vehicles', 'SellerProfile')
            SellerProfile.objects.create(user=instance)
        Notification = apps.get_model('notifications', 'Notification')
        Notification.objects.create(
            recipient=instance,
            message='Welcome to Cars Platform!',
            notification_type='info'
        )