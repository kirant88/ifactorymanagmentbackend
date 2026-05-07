from rest_framework import viewsets, permissions
from .models import Event, Collaboration, SocialMediaPost
from .serializers import EventSerializer, CollaborationSerializer, SocialMediaPostSerializer

class EngagementBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superadmin:
            queryset = queryset.filter(location=user.location)
        
        location_filter = self.request.query_params.get('location')
        if location_filter and location_filter != 'All Locations':
            queryset = queryset.filter(location__iexact=location_filter)
            
        return queryset

    def perform_create(self, serializer):
        location = self.request.user.location or 'Global'
        serializer.save(added_by=self.request.user, location=location)

class EventViewSet(EngagementBaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CollaborationViewSet(EngagementBaseViewSet):
    queryset = Collaboration.objects.all()
    serializer_class = CollaborationSerializer

class SocialMediaPostViewSet(EngagementBaseViewSet):
    queryset = SocialMediaPost.objects.all()
    serializer_class = SocialMediaPostSerializer

