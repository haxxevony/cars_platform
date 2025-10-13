from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SellerFeedback, SellerProfile, Vehicle, EVTelemetry
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=SellerFeedback)
def update_seller_rating(sender, instance, created, **kwargs):
    if created:
        seller = instance.seller
        profile = SellerProfile.objects.get(user=seller)
        feedbacks = SellerFeedback.objects.filter(seller=seller)
        avg_rating = feedbacks.aggregate(models.Avg('rating'))['rating__avg'] or 0.0
        profile.rating = round(avg_rating, 2)
        profile.save()

@receiver(post_save, sender=Vehicle)
def notify_vehicle_added(sender, instance, created, **kwargs):
    if created and instance.owner:
        subject = f'New Vehicle Added: {instance}'
        message = f'Your vehicle {instance.make} {instance.model} ({instance.year}) has been added to the Cars Platform.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.owner.email],
            fail_silently=True,
        )

@receiver(post_save, sender=EVTelemetry)
def notify_low_battery(sender, instance, created, **kwargs):
    if created and instance.battery_level < 20:
        vehicle = instance.vehicle
        if vehicle.owner:
            subject = f'Low Battery Alert for {vehicle}'
            message = f'Your vehicle {vehicle.make} {vehicle.model} has a battery level of {instance.battery_level}%. Please charge soon.'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [vehicle.owner.email],
                fail_silently=True,
            )