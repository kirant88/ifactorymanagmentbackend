from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_remove_training_attendees_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalmaturityassessment',
            name='payment_type',
            field=models.CharField(choices=[('PAID', 'Paid'), ('FREE', 'Free')], default='FREE', max_length=10),
        ),
        migrations.AddField(
            model_name='digitalmaturityassessment',
            name='photograph_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
