from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DailyPumpReportViewSet,
    WeeklySocialMediaReportViewSet,
    GlimpsesOfTheMonthViewSet,
)

router = DefaultRouter()
router.register(r"daily-pump", DailyPumpReportViewSet)
router.register(r"weekly-social", WeeklySocialMediaReportViewSet)
router.register(r"glimpses-month", GlimpsesOfTheMonthViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
