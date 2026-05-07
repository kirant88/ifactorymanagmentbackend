from rest_framework import viewsets, permissions
from .models import DailyPumpReport, WeeklySocialMediaReport, GlimpsesOfTheMonth
from .serializers import (
    DailyPumpReportSerializer,
    WeeklySocialMediaReportSerializer,
    GlimpsesOfTheMonthSerializer,
)


class DailyPumpReportViewSet(viewsets.ModelViewSet):
    queryset = DailyPumpReport.objects.all()
    serializer_class = DailyPumpReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, location=self.request.user.location)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        location = self.request.query_params.get("location")

        if user.role == "SUPERADMIN":
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
            return queryset

        # LOCATIONADMIN and others are locked to their own location
        return queryset.filter(location=user.location)


class WeeklySocialMediaReportViewSet(viewsets.ModelViewSet):
    queryset = WeeklySocialMediaReport.objects.all()
    serializer_class = WeeklySocialMediaReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, location=self.request.user.location)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        location = self.request.query_params.get("location")

        if user.role == "SUPERADMIN":
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
            return queryset

        # LOCATIONADMIN and others are locked to their own location
        return queryset.filter(location=user.location)


class GlimpsesOfTheMonthViewSet(viewsets.ModelViewSet):
    queryset = GlimpsesOfTheMonth.objects.all()
    serializer_class = GlimpsesOfTheMonthSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, location=self.request.user.location)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        location = self.request.query_params.get("location")

        if user.role == "SUPERADMIN":
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
            return queryset

        # LOCATIONADMIN and others are locked to their own location
        return queryset.filter(location=user.location)
