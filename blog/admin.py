from django.contrib import admin
from .models import BlogModel, BlogComment

# Register your models here.

admin.site.register(BlogModel)
admin.site.register(BlogComment)