from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'business_name', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'business_name']
    ordering = ['email']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'business_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
