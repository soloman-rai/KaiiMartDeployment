from django.urls import path
from .views import cart_home, update_cart


app_name = 'carts'

urlpatterns = [
    path('', cart_home, name='home'),
    path('update', update_cart, name='update'),
]