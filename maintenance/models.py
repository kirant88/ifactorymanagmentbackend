from django.db import models
from django.conf import settings

class Maintenance(models.Model):
    machine_name = models.CharField(max_length=200, default="Monthly Maintenance")
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100)
    date = models.CharField(max_length=100, null=True, blank=True) # Storing as string to match frontend 'November 2025'
    representative = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Store the entire checklist and inventory as JSON
    report_data = models.JSONField(default=dict)
    
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.organization_name} - {self.date}"
