from django.contrib import admin

from .models import RequestRecord


@admin.register(RequestRecord)
class RequestRecordAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'browser', 'location', 'isp', 'threat_detected', 'created_at')
    list_filter = ('threat_detected', 'created_at')
    search_fields = ('ip_address', 'browser', 'location', 'isp')
