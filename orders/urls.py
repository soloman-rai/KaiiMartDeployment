from django.urls import path

from .views import CheckoutView, ConfirmView, finalize, EsewaRequestView


app_name = 'orders'

urlpatterns = [
   path('', CheckoutView.as_view(), name='home'),
   path('confirm', ConfirmView.as_view(), name='confirm'),
   path('esewa-request/<str:id>', EsewaRequestView.as_view(), name='esewa-request'),
   path('final', finalize, name='final'), 
]