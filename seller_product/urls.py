"""seller_product URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

from product.views import home_view
from accounts.views import login_view
from seller.views import SupplierApplicationForm

from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
                                        PasswordResetDoneView,PasswordResetConfirmView,
                                        PasswordResetCompleteView)                                     

from django.conf import settings
from django.conf.urls.static import static


#Admin Title/Header/Index Configuration 
admin.site.site_header  = 'Kai Admin'
admin.site.site_title   = 'Kai Admin Panel'
admin.site.index_title  = 'Welcome To Kai Admin Panel'
admin.site.GRAPPELLI_ADMIN_TITLE = 'Kaii Admin'


#Main URL
urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('product/', include('product.urls', namespace='product')),
    path('seller/', include('seller.urls', namespace='seller')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('supplier_application_form', SupplierApplicationForm.as_view(), name='supplierform'),
    path('carts/', include('carts.urls', namespace='carts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('delivery/', include('delivery_team.urls', namespace='delivery')),
    path('manager/', include('manager.urls', namespace='manager')),
    path('kadmin/', include('Kadmin.urls', namespace='kadmin')),
    path('blog/', include('blog.urls', namespace='blog')),

    path('pwdcge/', PasswordChangeView.as_view(template_name='utils/change_password.html'),name='password_change'),
    path('pwdcge/done/', PasswordChangeDoneView.as_view(template_name='utils/password_change_done.html'), name='password_change_done'),
    path('pwd/reset/', PasswordResetView.as_view(),name='password_reset'),
    path('pwd_reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('pwd-reset/done/', PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)