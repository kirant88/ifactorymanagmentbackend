from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingViewSet, DigitalMaturityAssessmentViewSet

router = DefaultRouter()
router.register(r'assessment', DigitalMaturityAssessmentViewSet, basename='dma')
router.register(r'', TrainingViewSet, basename='training')

urlpatterns = [
    path('', include(router.urls)),
]
