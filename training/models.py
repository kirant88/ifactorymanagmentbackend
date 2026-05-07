from django.db import models
from django.conf import settings

class Training(models.Model):
    date = models.DateField()
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    industry_type = models.CharField(max_length=100, null=True, blank=True)
    person_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    photograph_link = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

class DigitalMaturityAssessment(models.Model):
    PAYMENT_CHOICES = [
        ('PAID', 'Paid'),
        ('FREE', 'Free'),
    ]

    organization_name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)
    total_assessments = models.IntegerField(default=0)
    total_impact = models.CharField(max_length=255)
    photograph_link = models.URLField(max_length=500, blank=True, null=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='FREE')
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
