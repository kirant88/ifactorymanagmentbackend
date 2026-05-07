from rest_framework import serializers
from .models import Training, DigitalMaturityAssessment

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'
        read_only_fields = ['added_by', 'location', 'created_at']

class DigitalMaturityAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalMaturityAssessment
        fields = '__all__'
        read_only_fields = ['added_by', 'location', 'created_at']
