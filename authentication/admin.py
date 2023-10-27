from django.contrib import admin
from .models import CustomUser, PasswordResetToken

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')

class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at')
    search_fields = ('user__username', 'token')
    list_filter = ('expires_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
