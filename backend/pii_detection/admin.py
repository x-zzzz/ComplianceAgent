from django.contrib import admin
from .models import PiiDetectionRecord

@admin.register(PiiDetectionRecord)
class PiiDetectionRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "risk_level", "created_at")
    search_fields = ("risk_level",)
    readonly_fields = ("created_at",)
