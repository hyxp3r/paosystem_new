from django.contrib import admin
from .models import PriemType, Program, DevelopeForm, Status, EduLevelProgram, Google, GoogleReport, Query, GoogleMonitoring, GoogleMonitoringFiles, AirtablePersonal, AirtableBases, AirtableTables,LogsCron



@admin.register(EduLevelProgram)
class EduLevelProgramAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(PriemType)
class PriemTypeAdmin(admin.ModelAdmin):

    list_display = ("name",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):

    list_display = ("code", "name")

@admin.register(DevelopeForm)
class DevelopeFormAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(Google)
class GoogleAdmin(admin.ModelAdmin):

    pass

@admin.register(GoogleReport)
class GoogleReportAdmin(admin.ModelAdmin):

    list_display = ("name",)

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
