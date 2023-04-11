from django.contrib import admin
from .models import PriemType, Program, DevelopeForm, Status, EduLevelProgram



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

