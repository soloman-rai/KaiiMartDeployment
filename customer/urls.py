from django.urls import path
from .views import (RegisterCustomerView, CustomerProfileView, customer_profile_edit,
                    registration_confirmation, CustomerSettingsView, customer_delete)

app_name = 'customer'

urlpatterns = [
    path('', CustomerProfileView.as_view(), name='home'),
    path('register-customer', RegisterCustomerView.as_view(), name='register'),
    path('edit-customer', customer_profile_edit, name='edit'), 
    path('confirm', registration_confirmation, name='confirm'),
    path('settings', CustomerSettingsView.as_view(), name='setting'),
    path('delete-account', customer_delete, name='delete_account'),
]