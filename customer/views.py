from django.shortcuts import render, redirect, HttpResponse

from .forms import CustomerRegisterForm, CustomerProfileEditForm, ContactUsForm
from .models import CustomerProfile, NewsletterSubscription, Enquiry
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.core.mail import send_mail
from django.template.loader import get_template
from seller_product.utils import otp_pin_generator
from django.contrib.auth import get_user_model


USER = get_user_model()

# Create your views here.

class RegisterCustomerView(CreateView):
    form_class = CustomerRegisterForm
    template_name = 'utils/register.html'
    context_object_name = 'form'
    success_url = reverse_lazy('customer:confirm')

    def form_valid(self, form):
        #Session to get user info
        self.request.session['email'] = form.cleaned_data['email']
        return super().form_valid(form)


def registration_confirmation(request):
    global otp_pin
    
    if request.method == 'POST':
        num = request.POST.get('otp', '')           
        if(num == otp_pin):
            del request.session['otp_pin']
            email = request.session.get('email')
            user = USER.objects.get(email=email)
            if user:
                user.is_active = True
                user.save()
                del request.session['email']
                return redirect('login')
        else:
            email = request.session.get('email')
            del request.session['otp_pin']
            user = USER.objects.filter(email=email)
            if user:
                user.delete()
                del request.session['email']
                return redirect('home')
    else:
        ##Prevent resubmission of email on page refresh   
        if not request.session.get('otp_pin'):
            email = request.session.get('email')
            otp_pin = otp_pin_generator()
            request.session['otp_pin'] = otp_pin
            context = {'otp_pin': otp_pin}
            send_mail(
                subject = 'Account Confirmation PIN',
                message = get_template('registration/email/customer_registration.txt').render(context),
                from_email = 'gaurab@email.com',
                recipient_list = [email],
            )
    return render(request, 'utils/otp_form.html')


class CustomerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/customer_home.html'


@login_required
def customer_profile_edit(request):
    if request.user.is_authenticated:
        form = CustomerProfileEditForm(instance=request.user.customerprofile)
        if request.method == 'POST':
            form = CustomerProfileEditForm(request.POST, request.FILES, instance=request.user.customerprofile)

            if form.is_valid():
                form.save()
            return redirect('customer:home')

        context = {'form': form}
        return render(request, 'customer/customer_profile_edit.html', context)
    else:
        return redirect('home')


class CustomerSettingsView(TemplateView):
    model = CustomerProfile
    template_name = 'customer/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = CustomerProfile.objects.get(user=self.request.user)
        context['customer'] = customer
        return context


def customer_delete(request):
    if request.method == "POST":
        cuser = CustomerProfile.objects.get(user=request.user)
        user = USER.objects.get(email=cuser)
        user.is_active = False
        user.save()
        cuser.delete()
        return redirect('home')
        
    return render(request, 'customer/delete_customer.html', {})


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST['user_email']

        subscription = NewsletterSubscription.objects.create(email=email)
        subscription.save()

        return HttpResponse('')   


# class ContactUsView(CreateView):
    form_class = ContactUsForm
    template_name = 'contact_us.html'
    # success_url = reverse_lazy('customer:contact_us')


def contact_us_view(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        p_num = request.POST['p_num']
        c_num = int(p_num)
        email = request.POST['email']
        message = request.POST['message']

        enquiry = Enquiry.objects.create(first_name=fname, last_name=lname, email=email, contact_number=c_num, message=message)
        enquiry.save()

        return HttpResponse('')


