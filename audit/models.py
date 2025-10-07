from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['method']),
            models.Index(fields=['status_code']),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} {self.method} {self.path} [{self.status_code}]"

    def __repr__(self):
        user_email = self.user.email if self.user else "anonymous"
        return f"<AuditLog {user_email} {self.method} {self.path} {self.status_code}>"
