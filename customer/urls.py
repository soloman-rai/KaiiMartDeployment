from django.urls import path
from .views import *

app_name = 'customer'

urlpatterns = [
    path('', CustomerProfileView.as_view(), name='home'),
    path('register-customer', RegisterCustomerView.as_view(), name='register'),
    path('edit-customer', customer_profile_edit, name='edit'), 
    path('confirm', registration_confirmation, name='confirm'),
    path('settings', CustomerSettingsView.as_view(), name='setting'),
    path('delete-account', customer_delete, name='delete_account'),
    path('subscribe_newsletter', subscribe_newsletter, name='subscribe_newsletter'),
    path('contact_us', TemplateView.as_view(template_name='contact_us.html'), name='contact_us'),
    path('contact_us_ajax', contact_us_view, name='contact_us_ajax'),
]