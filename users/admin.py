# from django.contrib import admin

# from django.contrib import admin
# from .models import UserProfile

# admin.site.register(UserProfile)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class CustomUserAdmin(UserAdmin):
    model = UserProfile
    # Show email and other fields in admin
    list_display = ['username', 'email', 'phone_number', 'date_of_birth', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(UserProfile, CustomUserAdmin)
