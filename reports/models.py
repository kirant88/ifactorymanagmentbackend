from django.db import models
from django.conf import settings


class DailyPumpReport(models.Model):
    date = models.DateField()
    po_numbers = models.JSONField(default=list)  # Store list of PO numbers
    reason = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Daily Pump Report - {self.date}"


class WeeklySocialMediaReport(models.Model):
    date = models.DateField()
    photo_link = models.URLField(max_length=500)
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Weekly Social Media Report - {self.date}"


class GlimpsesOfTheMonth(models.Model):
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    image_data = models.TextField()  # Base64 encoded image for minimal storage
    image_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-month"]
        unique_together = ["month", "year", "location"]

    def __str__(self):
        return f"Glimpses - {self.month}/{self.year} - {self.location}"
