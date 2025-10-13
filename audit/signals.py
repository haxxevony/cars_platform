from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.utils import timezone
from .models import AuditLog

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    if sender.__name__ in ['CustomUser', 'Vehicle', 'Notification']:
        AuditLog = apps.get_model('audit', 'AuditLog')
        action = 'created' if created else 'updated'
        AuditLog.objects.create(
            user=instance if sender.__name__ == 'CustomUser' else getattr(instance, 'owner', None),
            model_name=sender.__name__,
            instance_id=str(instance.pk),
            action=action,
            details=f"{sender.__name__} {action}: {str(instance)}",
            timestamp=timezone.now()
        )

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender.__name__ in ['CustomUser', 'Vehicle', 'Notification']:
        AuditLog = apps.get_model('audit', 'AuditLog')
        AuditLog.objects.create(
            user=instance if sender.__name__ == 'CustomUser' else getattr(instance, 'owner', None),
            model_name=sender.__name__,
            instance_id=str(instance.pk),
            action='deleted',
            details=f"{sender.__name__} deleted: {str(instance)}",
            timestamp=timezone.now()
        )