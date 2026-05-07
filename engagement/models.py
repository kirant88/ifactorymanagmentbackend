# from django.db import models
# from django.conf import settings

# class Event(models.Model):
#     category = models.CharField(max_length=100)
#     event_title = models.CharField(max_length=255)
#     date = models.DateField()
#     audience_type = models.CharField(max_length=100)
#     participants_count = models.IntegerField(default=0)
#     location = models.CharField(max_length=100)
#     added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-date']

# class Collaboration(models.Model):
#     partner_name = models.CharField(max_length=255)
#     partner_type = models.CharField(max_length=100)
#     purpose = models.TextField()
#     start_date = models.DateField()
#     status = models.CharField(max_length=50)
#     location = models.CharField(max_length=100)
#     added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-start_date']

# class SocialMediaPost(models.Model):
#     platform = models.CharField(max_length=100)
#     content_type = models.CharField(max_length=100)
#     post_date = models.DateField()
#     objective = models.TextField()
#     engagement = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-post_date']

from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    category = models.CharField(max_length=100)
    event_title = models.CharField(max_length=255)

    date = models.DateField(default=timezone.now)  # 👈 FIX

    audience_type = models.CharField(max_length=100)
    participants_count = models.IntegerField(default=0)
    photograph_link = models.URLField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(default=timezone.now)  # 👈 FIX

    class Meta:
        ordering = ["-date"]


class Collaboration(models.Model):
    partner_name = models.CharField(max_length=255)
    partner_type = models.CharField(max_length=100)
    purpose = models.TextField()

    start_date = models.DateField(default=timezone.now)  # 👈

    status = models.CharField(max_length=50)
    photograph_link = models.URLField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(default=timezone.now)  # 👈

    class Meta:
        ordering = ["-start_date"]


class SocialMediaPost(models.Model):
    platform = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)

    post_date = models.DateField(default=timezone.now)  # 👈

    objective = models.TextField()
    engagement = models.CharField(max_length=100)
    photograph_link = models.URLField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(default=timezone.now)  # 👈

    class Meta:
        ordering = ["-post_date"]
