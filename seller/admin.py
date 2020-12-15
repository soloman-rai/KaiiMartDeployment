from django.contrib import admin
from .models import SupplierProfile, SupplierForm

# Register your models here.

admin.site.register(SupplierProfile)
admin.site.register(SupplierForm)