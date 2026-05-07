import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifactory.settings')
django.setup()

print("Applying migrations...")
try:
    call_command('makemigrations')
    call_command('migrate')
    print("DONE")
except Exception as e:
    print(f"ERROR: {e}")
