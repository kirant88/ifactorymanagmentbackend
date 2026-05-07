from rest_framework import serializers
from .models import Event, Collaboration, SocialMediaPost

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['added_by', 'location', 'created_at']

class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = '__all__'
        read_only_fields = ['added_by', 'location', 'created_at']

class SocialMediaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPost
        fields = '__all__'
        read_only_fields = ['added_by', 'location', 'created_at']

