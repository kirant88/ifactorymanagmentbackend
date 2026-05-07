from rest_framework import serializers
from .models import DailyPumpReport, WeeklySocialMediaReport, GlimpsesOfTheMonth


class DailyPumpReportSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = DailyPumpReport
        fields = "__all__"


class WeeklySocialMediaReportSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = WeeklySocialMediaReport
        fields = "__all__"


class GlimpsesOfTheMonthSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = GlimpsesOfTheMonth
        fields = "__all__"
