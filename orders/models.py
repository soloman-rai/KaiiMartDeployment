import math
from django.db import models
from django.contrib.auth import get_user_model
from carts.models import Cart, CartItem

USER = get_user_model()

# Create your models here.

ORDER_CHOICES = (
    ('created', 'Created'),
    ('delivered', 'Delivered'),
    ('refunded', 'Refunded'),
)

class Order(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=50, blank=True)
    #Always use models.SET_NULL for ForeignKey. Donot use models.Do_Nothing, it will cause IntegrityError.
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_num = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    
    status = models.CharField(choices=ORDER_CHOICES, max_length=30, default='created')
    delivery_cost = models.DecimalField(default=50.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.order_id:
            return f'Order-Id: {self.order_id}'
        else:
            return str(self.id)   


    def order_total_cost(self):
        cart_total = self.cart.total
        delivery_cost = self.delivery_cost
        new_total = math.fsum([cart_total, delivery_cost])   #This is just a simple sum.Nothing else
        formatted_total = format(new_total, '.2f')  #String formatting with 2 digits of precision
        self.total = formatted_total
        self.save()
        return new_total