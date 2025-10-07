from django.contrib import admin
from .models import AuditLog

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'method', 'path', 'status_code', 'timestamp']
    list_filter = ['method', 'status_code']
    search_fields = ['user__email', 'path']
    readonly_fields = ['user', 'method', 'path', 'status_code', 'timestamp']
    ordering = ['-timestamp']

admin.site.register(AuditLog, AuditLogAdmin)
