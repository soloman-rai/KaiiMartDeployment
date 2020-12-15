# from django.db.models.signals import post_save
# from .models import Delivery
# from carts.models import Cart
# from orders.models import Order


# def post_save_order_receiver(sender, instance, created, *args, **kwargs):
#     cart_obj, new_cart_obj = Cart.objects.new_or_get(self.request)
#     if cart_obj:
#         order_obj = Order.objects.filter(cart=cart_obj).last()
#     if order_obj:
#         Delivery.objects.create(order=order_obj.order_id)
    
# post_save.connect(post_save_order_receiver, sender=Cart)
