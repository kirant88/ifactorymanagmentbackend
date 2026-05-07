import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifactory.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'training_digitalmaturityassessment';")
    cols = [row[0] for row in cursor.fetchall()]
    print(f"DMA Columns: {cols}")
    
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'engagement_collaboration';")
    cols = [row[0] for row in cursor.fetchall()]
    print(f"Engagement Collaboration Columns: {cols}")
