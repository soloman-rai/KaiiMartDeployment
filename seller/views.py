from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .models import SupplierProfile, SupplierForm
from .forms import SupplierRegisterForm, SupplierProfileEditForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView

from django.urls import reverse_lazy

# Create your views here.

USER = get_user_model()


class SupplierProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'seller/supplier_home.html'


@login_required
def supplier_profile_edit(request):

    if request.user.is_authenticated:
        form = SupplierProfileEditForm(instance=request.user.supplierprofile)

        if request.method == 'POST':
            form = SupplierProfileEditForm(request.POST, request.FILES, instance=request.user.supplierprofile)

            if form.is_valid():
                form.save()
            return redirect('seller:home')  

        context = {'form': form}
        return render(request, 'seller/supplier_profile_edit.html', context)      
    else:
        return redirect('home')
    
class SupplierSettingsView(LoginRequiredMixin, TemplateView):
    model = SupplierProfile
    template_name = 'seller/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = SupplierProfile.objects.get(user=self.request.user)
        context['seller'] = supplier
        return context


class SupplierApplicationForm(CreateView):
    model = SupplierForm
    fields = ['supplier_name', 'supplier_email', 'supplier_phone_num', 'shop_name', 'shop_address']
    template_name = 'seller/supplier_application_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.supplier_name = self.request.user.username
            form.instance.supplier_email = self.request.user
            # form.instance.save()
        messages.success(self.request, 'Your Application has been saved. Our team will contact you soon')
        return super().form_valid(form)   
