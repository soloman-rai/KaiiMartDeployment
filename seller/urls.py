from django.urls import path
from .views import SupplierProfileView, supplier_profile_edit, SupplierSettingsView 

app_name = 'seller'

urlpatterns = [
    path('', SupplierProfileView.as_view(), name='home'),
    path('edit-supplier', supplier_profile_edit, name='edit'),
    path('settings', SupplierSettingsView.as_view(), name='setting'),
]