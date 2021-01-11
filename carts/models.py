from django.db import models

from django.contrib.auth import get_user_model

from product.models import Product

# Create your models here.

USER = get_user_model()

#CartManager defines the new_or_get function that 
class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new_cart(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id 
        return cart_obj, new_obj           

    def new_cart(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)  


class Cart(models.Model):
    #Always use models.SET_NULL for ForeignKey. Donot use models.Do_Nothing, it will cause IntegrityError.
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ManyToManyField(Product, through='CartItem')
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total_saved_after_discount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = CartManager()

    def __str__(self):
        return f'Cart id: {self.id}'

    def update_total(self):
        items = self.cartitem_set.all()  #cartitem_set is used beacause of the many to many field between cart and product, it is provided by django
        total = 0
        for item in items:
            total += item.item_total_price
        self.total = "%.2f" %(total)
        self.save() 

    def update_saved_total(self):
        items = self.cartitem_set.all()
        total_saved_after_discount = 0 
        for item in items:
            total_saved_after_discount += item.item_total_saved_price 
        self.total_saved_after_discount = "%.2f" %(total_saved_after_discount)
        self.save()      


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total_price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    item_total_saved_price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.cart.id:
            return str(self.cart.id) 
        else:
            return f'CartItem:{self.id}' 
          

    

