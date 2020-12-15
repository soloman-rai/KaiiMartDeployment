from django.db.models.signals import pre_save, post_save
from .models import Order
from carts.models import Cart

# Changes in Cart_total also changes Order_total
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_total = instance.total
        cart_id = instance.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.order_total_cost()

post_save.connect(post_save_cart_total, sender=Cart)


# For first save 
def post_save_order_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.order_total_cost()
            
post_save.connect(post_save_order_total, sender=Order)  
