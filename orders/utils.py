import string
import random

from.models import Order



def order_id_generator():
    size = 7
    order_id = ""
    key = string.ascii_uppercase + string.digits + string.punctuation 
    for i in range(size):
        order_id = order_id + random.choice(key)

    try:
        order = Order.objects.get(order_id=order_id)
        order_id_generator()
    except Order.DoesNotExist:
        return order_id 