from django.urls import path
from .views import (ManagerHomeView, TagListView, DeleteTagView, ProductListView, ProductUpdateView,
                    DeleteProductView, CategoryListView, DeleteCategoryView, delivery_team_list,
                    DeleteDeliveryTeamView, supplier_list, SupplierFormView, SupplierFormUpdateView,
                    DeleteSupplierView, HomeSliderListView, OurProductsAreView, BlogCreateView,
                    BlogUpdateView, BlogDeleteView, ManagerSettingView)


app_name = 'manager'

urlpatterns = [
    path('', ManagerHomeView.as_view(), name='home'),
    path('home_sliders', HomeSliderListView.as_view(), name='home_sliders'),
    path('tag_list', TagListView.as_view(), name='tag_list'),
    path('delete-tag/<str:pk>', DeleteTagView.as_view(), name='delete_tag'),
    path('product-list', ProductListView.as_view(), name='product_list'),
    path('product-update/<str:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('delete-product/<str:pk>', DeleteProductView.as_view(), name='delete_product'),
    path('category-list', CategoryListView.as_view(), name='category_list'),
    path('delete-category/<str:pk>', DeleteCategoryView.as_view(), name='delete_category'),
    path('our_products_are', OurProductsAreView.as_view(), name='our_products_are'),
    path('delivery-team-list', delivery_team_list, name='delivery_team_list'),
    path('delete-delivery-team/<str:pk>', DeleteDeliveryTeamView.as_view(), name='delete_delivery_team'),
    path('supplier-list', supplier_list, name='supplier_list'),
    path('supplier-waiting-list', SupplierFormView.as_view(), name='supplier_waiting_list'),
    path('supplier-waiting-update/<str:pk>', SupplierFormUpdateView.as_view(), name='supplier_waiting_update'),
    path('delete-supplier/<str:pk>', DeleteSupplierView.as_view(), name='delete_supplier'),
    path('blog-create', BlogCreateView.as_view(), name='blog_create'),
    path('blog-update/<str:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog-delete/<str:pk>', BlogDeleteView.as_view(), name='blog_delete'),
    path('settings', ManagerSettingView.as_view(), name='settings'),
]