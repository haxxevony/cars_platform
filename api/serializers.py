from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from audit.models import AuditLog
from notifications.models import Notification
from vehicles.models import EVTelemetry

User = get_user_model()

# --- User Serializers ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'business_name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'business_name']

# --- Audit & Notification ---
class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'path', 'method', 'status_code', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'timestamp']
        read_only_fields = ['id', 'timestamp']

# --- Vehicle Telemetry ---
class EVTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EVTelemetry
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']
