# Engagement URLs
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CollaborationViewSet, SocialMediaPostViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'collaborations', CollaborationViewSet, basename='collaboration')
router.register(r'social-media', SocialMediaPostViewSet, basename='social-media')

urlpatterns = [
    path('', include(router.urls)),
]

