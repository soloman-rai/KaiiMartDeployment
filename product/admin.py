from django.contrib import admin
from .models import (Category, Product, Tag, ProductImage, Comment, Rating)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    list_display = ['title', 'slug']
    list_filter = ['title',]
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Category


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'tags']
    list_display = ['title', 'supplier', 'price', 'date_created', 'date_updated']
    list_filter = ['price', 'tags', 'supplier']
    prepopulated_fields = {'slug': ('title', )}

    class Meta:
        model = Product


class TagAdmin(admin.ModelAdmin):
    search_fields = ['title',]
    list_display = ['title', 'slug']
    list_filter = ['title',]
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = Tag


class RatingAdmin(admin.ModelAdmin):
    search_fields = ['product', 'user',]
    list_display = ['product', 'user',]
    list_filter = ['product', 'user',]

    class Meta:
        model = Rating


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Rating, RatingAdmin)