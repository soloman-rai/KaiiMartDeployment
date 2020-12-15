from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Delivery, DeliveryTeamProfile
from .forms import DeliveryTeamRegisterForm, DeliveryTeamProfileEditForm
from accounts.forms import LoginForm

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.
       
class DeliverTeamProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'delivery_team/delivery_team_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_delivery_team:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


@login_required
def deliverteam_profile_edit(request):
    if request.user.is_authenticated and request.user.is_delivery_team:
        form = DeliveryTeamProfileEditForm(instance=request.user.deliveryteamprofile)
        if request.method == 'POST':
            form = DeliveryTeamProfileEditForm(request.POST, request.FILES,
                                        instance=request.user.deliveryteamprofile)

            if form.is_valid():
                print(form.cleaned_data)
                form.save()
            return redirect('delivery:profile')

        context = {'form': form}
        return render(request, 'delivery_team/delivery_profile_edit.html', context)


class OrderDeliveryView(LoginRequiredMixin, ListView):
    model = Delivery
    template_name = 'delivery_team/home.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_delivery_team:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    #Get latest order first (i.e in descending order)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Delivery.objects.filter(order__status='created').order_by('-id')
        delivered_qs = Delivery.objects.filter(order__status='delivered').order_by('-id')
        refunded_qs = Delivery.objects.filter(order__status='refunded').order_by('-id')
        context['confirmed_qs'] = qs
        context['delivered_qs'] = delivered_qs
        context['refunded_qs'] = refunded_qs
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Delivery
    template_name = 'delivery_team/order_detail.html'
    # context_object_name = 'order'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_delivery_team:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['pk']
        qs = Delivery.objects.get(id=order_id)
        product_qs = qs.order.cart.cartitem_set.all()

        context['order'] = qs
        context['product'] = product_qs
        return context       


class DeliveryTeamSettingView(LoginRequiredMixin, TemplateView):
    model = Delivery
    template_name = 'delivery_team/settings.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_delivery_team:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')