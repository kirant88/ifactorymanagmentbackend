from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('engagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photograph_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='photograph_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='socialmediapost',
            name='photograph_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
