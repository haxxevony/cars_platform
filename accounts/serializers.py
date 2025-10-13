from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# 👤 UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'address',
            'bio',
            'profile_picture',
        ]
        read_only_fields = ['user', 'email', 'first_name', 'last_name', 'role']

# 🛠️ Optional: CustomUser Serializer (for admin APIs or future use)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']
