from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from customer.models import CustomerProfile
from product.models import Tag, Product, Category 
from delivery_team.models import DeliveryTeamProfile
from seller.models import SupplierProfile
from manager.models import Manager
from orders.models import Order
from carts.models import Cart, CartItem
from .models import KAdmin

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import ManagerRegisterForm
from product.forms import ProductCreateForm

from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

USER = get_user_model()

# Create your views here.

class AdminHomeView(ListView):
    model = KAdmin
    template_name = 'admin/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_qs = USER.objects.all().order_by('-id')
        customer = CustomerProfile.objects.all().order_by('-id')[:3]
        tags = Tag.objects.all().order_by('-id')[:3]        
        product = Product.objects.all().order_by('-id')[:3]       
        category = Category.objects.all().order_by('-id')[:3]     
        delivery_team = DeliveryTeamProfile.objects.all().order_by('-id')     
        supplier_profile = SupplierProfile.objects.all().order_by('-id')[:3]
        manager = Manager.objects.all().order_by('-id')[:3]
        order = Order.objects.all().order_by('-id')[:3]
        cart = Cart.objects.all().order_by('-id')
     
        context['user_qs'] = user_qs
        context['tags'] = tags
        context['product'] = product
        context['category'] = category
        context['delivery_team'] = delivery_team
        context['supplier_profile'] = supplier_profile
        context['manager'] = manager
        context['order'] = order
        context['cart'] = cart
        context['customer'] = customer

        return context

#CreateView and ListView of Manager

@login_required
def manager_list(request):
    if request.method == 'POST':
        form = ManagerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            form.save()

            context = {
                'username': username,
                'email': email,
                'password': password,
            }
            send_mail(           
                subject = 'Account Created',
                message = get_template('registration/email/registration_email.txt').render(context),
                from_email = 'gaurab@email.com',
                recipient_list = [email],
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    form = ManagerRegisterForm()
    qs = Manager.objects.all()
    context = {
        'form': form,
        'manager': qs,
    } 
    return render(request, 'admin/manager_list.html', context)        
             

class DeleteManagerView(LoginRequiredMixin, DeleteView):
    model = Manager
    template_name = 'admin/delete_manager.html'
    success_url = reverse_lazy('kadmin:manager-list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")


class UserStatusView(LoginRequiredMixin, ListView):
    model = USER
    template_name = 'admin/users_status.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_user_qs = USER.objects.filter(is_active=True).order_by('-id')
        inactive_user_qs = USER.objects.filter(is_active=False).order_by('-id')
        context['active_user'] = active_user_qs
        context['inactive_user'] = inactive_user_qs
        return context


class UserStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = USER
    fields = '__all__'
    template_name = 'admin/users_status_update.html'
    success_url = reverse_lazy('kadmin:users_list')        

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")


