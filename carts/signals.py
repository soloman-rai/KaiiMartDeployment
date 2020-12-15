from .models import Cart,CartItem

from decimal import Decimal
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


def pre_save_cart_item_receiver(sender, instance, *args, **kwargs):
        qty = instance.quantity
        total_price = 0
        total_save = 0
        if int(qty) >=1:
            if instance.product.discount_price:
                price = instance.product.price-instance.product.discount_price
            else:
                price = instance.product.price

            if instance.product.discount_price:
                total_save += Decimal(qty) * Decimal(instance.product.discount_price)
                instance.item_total_saved_price = total_save 
                
            total_price += Decimal(qty) * Decimal(price)
            instance.item_total_price= total_price

pre_save.connect(pre_save_cart_item_receiver, sender=CartItem)


def post_save_cart_item_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_total()

post_save.connect(post_save_cart_item_receiver, sender=CartItem)

post_delete.connect(post_save_cart_item_receiver, sender=CartItem)