from django.urls import path

from .views import CheckoutView, ConfirmView, finalize


app_name = 'orders'

urlpatterns = [
   path('', CheckoutView.as_view(), name='home'),
   path('confirm', ConfirmView.as_view(), name='confirm'),
   path('final', finalize, name='final'), 
]