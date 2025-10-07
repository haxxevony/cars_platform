from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'business_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['business_name'].widget.attrs.update({'class': 'form-control'})
