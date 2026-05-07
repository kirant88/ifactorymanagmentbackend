from rest_framework import viewsets, permissions
from .models import Maintenance
from .serializers import MaintenanceSerializer

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Maintenance.objects.all()
        if not user.is_superadmin:
            queryset = queryset.filter(location=user.location)
        
        location_filter = self.request.query_params.get('location')
        if location_filter and location_filter != 'All Locations':
            queryset = queryset.filter(location__iexact=location_filter)
            
        return queryset

    def perform_create(self, serializer):
        location = self.request.user.location or 'Global'
        serializer.save(added_by=self.request.user, location=location)
