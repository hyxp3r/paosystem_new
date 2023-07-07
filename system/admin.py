from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Google)
class GoogleAdmin(admin.ModelAdmin):

    pass


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(GoogleMonitoring)
class GoogleMonitoringAdmin(admin.ModelAdmin):

    list_display = ("name", "status")

@admin.register(GoogleMonitoringFiles)
class GoogleMonitoringFilesAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(AirtablePersonal)
class AirtablePersonalAdmin(admin.ModelAdmin):

    pass

@admin.register(AirtableBases)
class AirtableBasesAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(AirtableTables)
class AirtableTablesAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(LogsCron)
class LogsCronAdmin(admin.ModelAdmin):

    list_display = ("name", "status", "created_at")
