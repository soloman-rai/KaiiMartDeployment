from orders.models import Order
import string
import random

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

def otp_pin_generator():
    otp_pin = ''
    for i in range(4):
        num = random.randrange(0, 10)
        otp_pin += str(num)
    return otp_pin

            