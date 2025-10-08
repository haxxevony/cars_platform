import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_platform.settings")
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

# Run migrations
call_command("migrate")

# Create superuser if not exists
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="Haxxy",
        email="haxxevony@gmail.com",
        password="NewSecurePassword123"
    )
