from django.contrib import admin
from .models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'admin', 'staff', 'is_customer', 'is_supplier', 'is_delivery_team',
                    'is_manager', 'date_joined', 'last_login', )
    list_filter = ('admin', 'staff', 'is_active', 'is_customer', 'is_supplier', 'is_delivery_team',
                    'is_manager')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_customer', 'is_supplier', 'is_delivery_team', 'is_manager',
                                    'admin', 'staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide', ),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)