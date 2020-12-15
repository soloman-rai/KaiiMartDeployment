from django.urls import path
from .views import (AdminHomeView,DeleteManagerView, manager_list, UserStatusView,
                    UserStatusUpdateView)

app_name='kadmin'

urlpatterns = [
    path('', AdminHomeView.as_view(), name='home'),
    path('users-list', UserStatusView.as_view(), name='users_list'),
    path('users-status-update/<str:pk>', UserStatusUpdateView.as_view(), name='users_status_update'),
    path('manager-list', manager_list, name='manager-list'),
    path('delete-manager/<str:pk>', DeleteManagerView.as_view(), name='delete-manager'),
]