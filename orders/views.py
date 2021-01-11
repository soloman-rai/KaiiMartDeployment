from django.shortcuts import render, redirect, get_object_or_404

from .models import Order
from carts.models import Cart

from seller_product.utils import order_id_generator

from django.views.generic import TemplateView, CreateView, View
from django.urls import reverse_lazy

from delivery_team.models import Delivery

# Create your views here.

class CheckoutView(CreateView):
    model = Order
    template_name = 'checkout/place_order.html'
    fields = ['full_name', 'email', 'phone_num', 'city', 'address']
    context_object_name = 'form'
    success_url = reverse_lazy('orders:confirm')

    def dispatch(self, request, *args, **kwargs):
        cart_obj, new_cart_obj = Cart.objects.new_or_get(request)
        if new_cart_obj or cart_obj.product.count() == 0:
            return redirect("carts:home")
            # Todo ..message: Your cart is empty

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cart_obj, new_cart_obj = Cart.objects.new_or_get(self.request)    
        if cart_obj:
            # If user is authentic then replace order_user with it else leave it empty
            if self.request.user.is_authenticated:
                form.instance.fullname = self.request.user.username
                form.instance.email = self.request.user.email
            form.instance.cart = cart_obj
            form.instance.order_id = order_id_generator()
            form.save()
        return super().form_valid(form) 
           
class PaymentSelectView(TemplateView):
    template_name = 'checkout/choose_payment_method.html'

class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.GET.get("id")
        cart_obj, new_cart_obj = Cart.objects.new_or_get(self.request)
        if cart_obj:
            order_obj = Order.objects.filter(cart=cart_obj).last()
        context = {
            "order": order_obj    
        }
        return render(request, "checkout/esewa_request.html", context)

class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        oid = request.GET.get('oid')
        amt = request.GET.get('amt')
        refId = request.GET.get('refId')
        return reverse('orders:final')

#Checkout Step to show user info and proceed to cart deletion
class ConfirmView(TemplateView):
    template_name = 'checkout/order_confirm.html'
    success_url = reverse_lazy('orders:final')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_cart_obj = Cart.objects.new_or_get(self.request)
        if cart_obj:
            order_obj = Order.objects.filter(cart=cart_obj).last()
        context['order'] = order_obj   
        return context

    def form_valid(self):
        return super().form_valid(form)

# Final step for checkout to delete Cart 
def finalize(request):
    cart_obj, new_cart_obj = Cart.objects.new_or_get(request)
    if cart_obj:
        order_obj = Order.objects.filter(cart=cart_obj).last()
    
    if 'confirm' in request.POST:
        request.session['items_total'] = 0

        delivery = Delivery.objects.create(order=order_obj, total=order_obj.total)
        delivery.save()
    
    return render(request, 'checkout/finalize.html')       
 
