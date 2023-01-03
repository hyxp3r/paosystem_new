from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'dateBith')
        }),
        ('Права', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Системные даты', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Служебная информация', {
            'fields': ('department', 'post')
        })
    )

admin.site.register(User, CustomUserAdmin)
