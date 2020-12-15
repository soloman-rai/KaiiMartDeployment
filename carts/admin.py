from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_created', 'date_updated')
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
