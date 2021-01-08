from django.shortcuts import render, redirect
from .models import Manager, HomeTopSlider, OurProductsAre

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from product.forms import ProductCreateForm
from delivery_team.forms import DeliveryTeamRegisterForm
from seller.forms import SupplierRegisterForm

from product.models import Tag,Product, Category 
from delivery_team.models import DeliveryTeamProfile
from seller.models import SupplierProfile, SupplierForm
from blog.models import BlogModel

from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from django.contrib.auth.decorators import login_required

# Create your views here.

class ManagerHomeView(LoginRequiredMixin, ListView):
    model = Manager
    template_name = 'manager/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all().order_by('-id')[:3]        
        product = Product.objects.all().order_by('-id')[:3]
        home_slider = HomeTopSlider.objects.all().order_by('-id')[:3]  
        our_products_are = OurProductsAre.objects.all()    
        category = Category.objects.all().order_by('-id')[:3]     
        delivery_team = DeliveryTeamProfile.objects.all().order_by('-id')     
        supplier_profile = SupplierProfile.objects.all().order_by('-id')[:3]
        supplier_waiting_list = SupplierForm.objects.all().order_by('-id')[:3]
        blog = BlogModel.objects.all().order_by('-id')[:5]
     
        context['tags'] = tags
        context['product'] = product
        context['home_slider'] = home_slider
        context['category'] = category
        context['our_products_are'] = our_products_are
        context['delivery_team'] = delivery_team
        context['supplier_profile'] = supplier_profile
        context['supplier_waiting_list'] = supplier_waiting_list
        context['blog'] = blog

        return context


#Home Main Sliders##
#List Sliders and create more sliders
class HomeSliderListView(LoginRequiredMixin, CreateView):
    model = HomeTopSlider
    fields = ['title', 'image', 'detail']
    template_name = 'manager/home_sliders.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = HomeTopSlider.objects.all()
        context['sliders'] = sliders
        return context 
    
    #Redirect to same page
    def get_success_url(self):
        return reverse('manager:home_sliders')    


#Our Products Are
#List and create 
class OurProductsAreView(LoginRequiredMixin, CreateView):
    model = OurProductsAre
    fields = ['image', 'info']
    template_name = 'manager/our_products_are.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info = OurProductsAre.objects.all()
        context['info'] = info
        return context 
    
    #Redirect to same page
    def get_success_url(self):
        return reverse('manager:our_products_are')  


##Tags View##
#Shows List of tags and allows to add tags 
class TagListView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['title']
    template_name = 'manager/tags_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        tags = Tag.objects.all().order_by('-id')
        context['tags'] = tags
        return context   

    #Redirect to same page
    def get_success_url(self):
        return reverse('manager:tag_list')


class DeleteTagView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'manager/delete_tag.html'
    success_url = reverse_lazy('manager:tag_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


############

##Product View##

#Shows List of products and allows to add product 
class ProductListView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'manager/product_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return context

    def get_success_url(self): 
        return reverse('manager:product_list')   


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'manager/product_update.html'
    context_object_name = 'product'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')    

    def get_success_url(self):
        return reverse('manager:product_list') 


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'manager/delete_product.html'
    success_url = reverse_lazy('manager:product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')

##########################################
   
##Category View##

#Shows List of categories and allows to add category 
class CategoryListView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['parent', 'title']
    template_name = 'manager/category_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return context 

    def get_success_url(self):
        return reverse('manager:category_list')    


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'manager/delete_category.html'
    success_url = reverse_lazy('manager:category_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


##########################################
      
##Delivery Team View##

#Shows List of Delivery Team and allows to add Delivery Team 
##Refactor this code to CBV. See earlier commits to check error in CBV process.
@login_required
def delivery_team_list(request):
    if request.user.is_authenticated and request.user.is_manager:
        if request.method == "POST":
            form = DeliveryTeamRegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                form.save()

                context = {
                    'username': username,
                    'email': email,
                    'password': password,
                    # 'site_url': settings.base.py.SITE_URL
                }
                send_mail(           
                    subject = 'Account Created',
                    message = get_template('registration/email/registration_email.txt').render(context),
                    from_email = 'gaurab@email.com',
                    recipient_list = [email],
                ) 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))         
        
        qs = DeliveryTeamProfile.objects.all().order_by('-id') 
        form = DeliveryTeamRegisterForm()
        context = {
            'deliveryteamprofile': qs,
            'form': form,  
        } 
        return render(request, 'manager/delivery_team_list.html', context)  
    else:
        return redirect('login')         


class DeleteDeliveryTeamView(LoginRequiredMixin, DeleteView):
    model = DeliveryTeamProfile
    template_name = 'manager/delete_delivery_team.html'
    success_url = reverse_lazy('manager:delivery_team_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


##########################################
        
##Supplier Team View##

#Shows List of Supplier Team and allows to add Supplier Team 
##Refactor this code to CBV. See earlier commits to check error in CBV process.
@login_required
def supplier_list(request):
    if request.user.is_authenticated and request.user.is_manager:
        if request.method == 'POST':
            form = SupplierRegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                form.save()

                context = {
                    'username': username,
                    'email': email,
                    'password': password,
                    # 'site_url': settings.base.py.SITE_URL
                }
                send_mail(           
                    subject = 'Account Created',
                    message = get_template('registration/email/registration_email.txt').render(context),
                    from_email = 'gaurab@email.com',
                    recipient_list = [email],
                ) 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

        form = SupplierRegisterForm()       
        qs = SupplierProfile.objects.all().order_by('-id')
        context = {
            'form': form,
            'supplierprofile': qs
        }
        return render(request, 'manager/supplier_list.html', context)
    else:
        return redirect('login')    


class DeleteSupplierView(LoginRequiredMixin, DeleteView):
    model = SupplierProfile
    template_name = 'manager/delete_supplier.html'
    success_url = reverse_lazy('manager:supplier_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


class SupplierFormView(LoginRequiredMixin, ListView):
    model = SupplierForm
    template_name = 'manager/supplier_form.html'   

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_waiting = SupplierForm.objects.filter(status='waiting').order_by('-id')
        qs_ignored = SupplierForm.objects.filter(status='ignore').order_by('-id')
        qs_accepted = SupplierForm.objects.filter(status='accept').order_by('-id')
        context['status_waiting'] = qs_waiting
        context['status_ignored'] = qs_ignored
        context['status_accepted'] = qs_accepted
        return context


class SupplierFormUpdateView(LoginRequiredMixin, UpdateView):
    model = SupplierForm
    fields = ['status', 'supplier_name', 'supplier_email', 'supplier_phone_num', 'shop_name', 'shop_address']
    template_name = 'manager/supplier_waiting_update.html'
    success_url = reverse_lazy('manager:supplier_waiting_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogModel
    fields = ['username', 'post_title', 'post_text', 'image', 'category']
    template_name = 'manager/blog_create.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = BlogModel.objects.all()
        context['blog'] = qs
        return context          

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse('manager:blog_create')      


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogModel
    fields = ['username', 'post_title', 'post_text', 'image', 'category']
    template_name = 'manager/blog_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['pk']
        qs = BlogModel.objects.get(id=blog_id)
        context['blog'] = qs
        return context

    def get_success_url(self):
        return reverse('manager:blog_create') 


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogModel
    template_name = 'manager/blog_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')
    
    def get_success_url(self):
        return reverse('manager:blog_create')


class ManagerSettingView(LoginRequiredMixin, TemplateView):
    model = Manager
    template_name = 'manager/settings.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')