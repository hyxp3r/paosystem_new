from django.contrib import admin
from .models import Department, Expert, ContractNames, CheckEc, Post

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("name",)

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):

    list_display = ("fioExpert","department")

@admin.register(ContractNames)
class ContractNamesAdmin(admin.ModelAdmin):

    list_display = ("sectionEC","expertEC")

@admin.register(CheckEc)
class CheckEcAdmin(admin.ModelAdmin):

    list_display = ("contractName",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ("name",)



