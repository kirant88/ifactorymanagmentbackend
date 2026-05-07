import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifactory.settings')
django.setup()

try:
    print("Running makemigrations...")
    call_command('makemigrations', 'training', 'engagement', 'accounts')
    print("Running migrate...")
    call_command('migrate')
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
