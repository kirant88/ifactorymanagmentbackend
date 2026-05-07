from django.db import models
from django.conf import settings
from django.utils import timezone

class Visitor(models.Model):
    PURPOSE_CHOICES = [
        ('MEETING', 'Meeting'),
        ('TRAINING', 'Training'),
        ('MAINTENANCE', 'Maintenance'),
        ('SITE_VISIT', 'Site Visit'),
        ('INDUSTRIAL', 'Industrial'),
        ('ACADEMIC', 'Academic'),
        ('GOVERNMENT', 'Government'),
        ('OTHER', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=200)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    categories = models.CharField(max_length=100, null=True, blank=True)
    industry_type = models.CharField(max_length=100, null=True, blank=True)
    photograph_link = models.URLField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-check_in']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
