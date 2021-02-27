from django.contrib import admin

from logger.models import LogRecord


admin.site.site_header = 'Hillel Post administration'


@admin.register(LogRecord)
class LogRecordAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'execution_time_sec')
    date_hierarchy = 'created'
    exclude = ('method', 'path', 'execution_time_sec', 'created')
    list_display_links = ('path',)
