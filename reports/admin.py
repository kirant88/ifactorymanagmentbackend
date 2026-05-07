from django.contrib import admin
from .models import DailyPumpReport, WeeklySocialMediaReport, GlimpsesOfTheMonth


@admin.register(DailyPumpReport)
class DailyPumpReportAdmin(admin.ModelAdmin):
    list_display = ("date", "location", "added_by", "created_at")
    list_filter = ("location", "date")
    search_fields = ("reason", "po_numbers")


@admin.register(WeeklySocialMediaReport)
class WeeklySocialMediaReportAdmin(admin.ModelAdmin):
    list_display = ("date", "location", "added_by", "created_at")
    list_filter = ("location", "date")
    search_fields = ("photo_link",)


@admin.register(GlimpsesOfTheMonth)
class GlimpsesOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "location", "image_name", "added_by", "created_at")
    list_filter = ("location", "year", "month")
    search_fields = ("image_name",)
