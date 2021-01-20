from django.urls import path
from .views import *


app_name = 'delivery'

urlpatterns = [
    path('', OrderDeliveryView.as_view(), name='home'),
    path('profile/', DeliverTeamProfileView.as_view(), name='profile'),
    path('profile-edit/', deliverteam_profile_edit, name='edit-profile'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='detail'),
    path('update_order/<int:pk>/', OrderStatusUpdateView.as_view(), name='update_order_status'),
    path('settings/', DeliveryTeamSettingView.as_view(), name='settings'),
]