from django.shortcuts import render, redirect, get_object_or_404

from product.models import Product
from .models import Cart, CartItem
from orders.models import Order

from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    # For showing cart count in navbar / Go to navabar.html to see its use    
    request.session['items_total'] = cart_obj.product.count()
    
    context = {
        'cart': cart_obj
    }

    return render(request, 'carts/home.html', context)

 
def update_cart(request):
    product_id = request.POST.get('products_id')
    
    delete_product = request.POST.get('remove', False)

    if product_id is not None:
        cart_obj, new_obj = Cart.objects.new_or_get(request)     
        try:
            product_obj = Product.objects.get_or_create(id=product_id)
        except Product.DoesNotExist:
            print('Sorry, the product you want is not in Stock. Try again after few days')
            return redirect('home')
    
        if 'add' in request.POST:
            cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product_id=product_id)
            qty = request.POST.get('qty')

            try:
                if int(qty) < 1:
                    delete_product = True
            except:
                raise Http404
            
            if delete_product:
                cart_item.delete()
                return redirect('carts:home')    

            if created:
                messages.info(request, 'Item was added successfully')
            else:
                messages.info(request, 'Item quantity was updated')
                cart_item.quantity = qty
                cart_item.save()

            request.session['items_total'] = cart_obj.product.count()   
   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirects to same(current) Page
