from django.urls import path
from .views import (DeliverTeamProfileView, deliverteam_profile_edit,
                    OrderDeliveryView, OrderDetailView, DeliveryTeamSettingView)


app_name = 'delivery'

urlpatterns = [
    path('', OrderDeliveryView.as_view(), name='home'),
    path('profile', DeliverTeamProfileView.as_view(), name='profile'),
    path('profile-edit', deliverteam_profile_edit, name='edit-profile'),
    path('detail/<str:pk>', OrderDetailView.as_view(), name='detail'),
    path('settings', DeliveryTeamSettingView.as_view(), name='settings'),
]