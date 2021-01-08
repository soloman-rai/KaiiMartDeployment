from django.shortcuts import render, redirect, get_object_or_404

from manager.models import HomeTopSlider, OurProductsAre
from .models import (Product, Tag, ProductImage, Comment, Rating, Category)
from .forms import ProductCreateForm
from carts.models import Cart, CartItem
from blog.models import BlogModel
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView 

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib import messages

from product.templatetags import custom_tags

from django.db.models import Q

from django.utils.timezone import now
from datetime import timedelta

# Create your views here.

USER = get_user_model()

#Home Page View
def home_view(request):

    #Home Slider
    slider = HomeTopSlider.objects.all()
    #nyano organic
    organic = Product.objects.filter(is_organic_store=True)[:8]
    #Categories
    category = Category.objects.all()
    #Our Products Are
    our_products_are = OurProductsAre.objects.all()
    #Latest Products
    latest_product = Product.objects.all().order_by('-id')[:10]
    #Blogs
    blog = BlogModel.objects.all().order_by('-id')[:3]

    ##Find best place to keep cart deletion code    
    #Auto delete cart after creation of 1 day
    Cart.objects.filter(date_created__lte=now()-timedelta(days=1)).delete()

    #Colors on tags
    color = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

    context = {
        'slider': slider,
        'organic': organic,
        'product': latest_product,
        'category': category,
        'our_products_are': our_products_are,
        'color': color,
        'blog': blog,
    }
    return render(request, 'home.html', context)


class organicstoreListView(ListView):
    model = Product
    template_name = 'product/organic_store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Product.objects.filter(is_organic_store=True)
        context['organic_store'] = qs
        return context


def organic_store_detail(request, pk):
    product = Product.objects.get(id=pk, is_organic_store=True)
    
    ##Rafactor Rating Code if possible
    #Product Rating On Product Detail
    rating_qs = Rating.objects.filter(product=product)
    if rating_qs:
        for x in rating_qs:
            not_rated = False
            rating = x.rating
    else:
        not_rated = True
        rating = 0

    #For Adding product to Cart
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    #For Comments and replies display
    comments = Comment.objects.filter(product=product, parent=None)
    replies = Comment.objects.filter(product=product).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)

    ####Refactor this query if possible####
    #For recommending similar products on the basis of tags
    tags_of_product = product.tags.all()
    similar_products_query = []
    similar_products = None

    #List of queries of products
    for tag in tags_of_product:
        qs = Product.objects.filter(tags__title__contains=tag.title).exclude(id=product.id)
        if qs:
            similar_products_query.append(qs)
    #Query of products
    if similar_products_query:        
        for item in similar_products_query:
            similar_products = item
    
    product_and_rating={}
    #Ratings of similar products
    if similar_products is not None:
        for x in similar_products:
            rating_qs = Rating.objects.filter(product=x)
            if rating_qs:
                for rx in rating_qs:
                    product_and_rating[x] = rx.rating
            else:
                product_and_rating[x] = 0 
            
    #########################################     
    #For colors in tags
    color = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

    context = {
        'product': product,
        'cart': cart_obj,
        'color': color,
        'rating': range(rating),
        'no_rating': range(5-rating),
        'not_rated': not_rated,
        'comments': comments,
        'reply': replyDict,
        'similar_items': similar_products,
        'product_rating': product_and_rating.items(),
    }
    return render(request, 'product/organic_store_detail.html', context)

#Shop Page View
def shop_page_view(request):
    product = Product.objects.all()

    #Categories
    category = Category.objects.all()

    ##Find best place to keep cart deletion code    
    #Auto delete cart after creation of 1 minute
    Cart.objects.filter(date_created__lte=now()-timedelta(days=1)).delete()
    
    ##Color on tags
    color = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

    context = {
        'product': product,
        'category': category,
        'color': color,
    }
    return render(request, 'product/shop_page.html', context)


#Product CRUD Section Starts
class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.supplier = self.request.user
        p = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            ProductImage.objects.create(product=p, image=i)        
        return super().form_valid(form) 

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    
    ##Rafactor Rating Code if possible
    #Product Rating On Product Detail
    rating_qs = Rating.objects.filter(product=product)
    if rating_qs:
        for x in rating_qs:
            not_rated = False
            rating = x.rating
    else:
        not_rated = True
        rating = 0

    #For Adding product to Cart
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    #For Comments and replies display
    comments = Comment.objects.filter(product=product, parent=None)
    replies = Comment.objects.filter(product=product).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)

####Refactor this query if possible####
    #For recommending similar products on the basis of tags
    tags_of_product = product.tags.all()
    similar_products_query = []
    similar_products = None

    #List of queries of products
    for tag in tags_of_product:
        qs = Product.objects.filter(tags__title__contains=tag.title).exclude(id=product.id)
        if qs:
            similar_products_query.append(qs)
    #Query of products
    if similar_products_query:        
        for item in similar_products_query:
            similar_products = item
    
    product_and_rating={}
    #Ratings of similar products
    if similar_products is not None:
        for x in similar_products:
            rating_qs = Rating.objects.filter(product=x)
            if rating_qs:
                for rx in rating_qs:
                    product_and_rating[x] = rx.rating
            else:
                product_and_rating[x] = 0 
            
#########################################     
    #For colors in tags
    color = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

    context = {
        'product': product,
        'cart': cart_obj,
        'color': color,
        'rating': range(rating),
        'no_rating': range(5-rating),
        'not_rated': not_rated,
        'comments': comments,
        'reply': replyDict,
        'similar_items': similar_products,
        'product_rating': product_and_rating.items(),
    }
    return render(request, 'product/product_detail.html', context)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'product/product_update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.supplier = self.request.user       
        
        product = self.get_object() 
        
        # Clear existing images
        for post_image in ProductImage.objects.filter(product=product):
            post_image.delete()
        
        # Updating new images
        images = self.request.FILES.getlist('more_images')        
        for i in images:
            ProductImage.objects.create(product=product, image=i)

        form.save()
        return super().form_valid(form)

    # If user is supplier update the product
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.supplier:
            return True
        return False    

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('home')
    template_name = 'product/product_delete.html'

    # If user is supplier delete the product
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.supplier:
            return True
        return False    
#Product CRUD Section Ends


#Category Wise Product Start
class CategoryProductView(ListView):
    model = Category
    template_name = 'product/category_wise_product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['pk']
        qs = Product.objects.filter(category=category)   
        context['product'] = qs
        return context
#Category Wise Product End


#Product Search Section
class ProductSearchResultView(ListView):
    model = Product
    template_name = 'product_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(season_choice__icontains=query) | 
            Q(tags__title__icontains=query) | Q(title__startswith=query)
        )
        return object_list


#Supplier's Product List Section
class SupplierProductsListView(ListView):
    model = Product
    template_name = 'product/all_products_of_supplier.html'
    context_object_name = 'product'

    def get_queryset(self):
        user = get_object_or_404(USER, email=self.kwargs.get('email'))
        # print(Product.objects.filter(supplier=user))
        return Product.objects.filter(supplier=user).order_by('date_created')


#Posting Rating on product
def rate_product(request):
    if request.method == "POST":
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        obj = Product.objects.get(id=el_id)
        rate = Rating.objects.create(product=obj, rating=val)
        rate.save()
        return JsonResponse({'success': 'true', 'rating': val}, safe=False)
    return JsonResponse({'success': 'false'})


# Comment Section
def create_comment(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
                user = request.user
                body = request.POST.get('body')
                product_id = request.POST.get('product_id')
                comment_id = request.POST.get('comment_id')
                product = Product.objects.get(id=product_id) 
                if comment_id == '':
                    comment = Comment.objects.create(user=user, product=product, body=body, name=user.username)
                    comment.save()
                    messages.success(request, "Your comment has been posted successfully")
                else:
                    parent = Comment.objects.get(id=comment_id)
                    print(parent)
                    comment = Comment.objects.create(user=user, product=product, body=body, name=user.username, parent=parent)
                    print(comment.name)
                    comment.save()
                    messages.success(request, "Your Reply has been posted successfully")
        return redirect(f'detail/{product_id}')          
    else:
        messages.info(request, "You must LogIn to post comment")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))         

  

# def similar_tags(request, slug):
#     tag = Tag.objects.get(slug__iexact=slug)
#     context = {'tag': tag}

#     return render(request, '', context)