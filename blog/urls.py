from django.urls import path
from .views import BlogListView, BlogDetailView, create_comment


app_name='blog'

urlpatterns = [
    path('', BlogListView.as_view(), name="home"),
    path('detail/<str:pk>', BlogDetailView.as_view(), name="detail"),
    path('comment', create_comment, name='comment'),
]