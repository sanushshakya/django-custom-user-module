from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name')
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name','last_name', 'password')}),
        ('Permissions', {'fields': ( 'is_active', 'is_staff', 'is_superuser')}),
        ('Timestamps', {'fields': ('date_joined',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)