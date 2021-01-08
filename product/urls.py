from django.urls import path
from .views import (organicstoreListView, organic_store_detail, shop_page_view, CreateProductView,
    product_detail, ProductUpdateView, ProductDeleteView, SupplierProductsListView,
    create_comment, ProductSearchResultView, rate_product, CategoryProductView)


app_name = 'product'

urlpatterns = [
    path('organic-store', organicstoreListView.as_view(), name='organic_store'),
    path('organic-detail/<str:pk>', organic_store_detail, name='organic_detail'),
    path('shop', shop_page_view, name='shop_page'),
    path('create', CreateProductView.as_view(), name='create'),
    path('detail/<str:pk>', product_detail, name='detail'),
    path('update/<str:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<str:pk>', ProductDeleteView.as_view(), name='delete'),
    path('all-products/<str:email>', SupplierProductsListView.as_view(), name='all_products'),
    path('comment', create_comment, name='comment'),
    path('search/', ProductSearchResultView.as_view(), name='search'),
    path('rate-product', rate_product, name='rate-product'),
    path('catproduct/<str:pk>', CategoryProductView.as_view(), name='cat-product'),
]