from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        user_display = self.recipient.username if self.recipient else "Anonymous"
        return f"To {user_display}: {self.message[:50]}"
