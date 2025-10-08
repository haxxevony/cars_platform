import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_platform.settings")
django.setup()

from django.core.management import call_command

call_command("migrate")
call_command("createsuperuser", interactive=True)
