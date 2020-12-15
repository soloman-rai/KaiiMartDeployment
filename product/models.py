from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth import get_user_model
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
from embed_video.fields import EmbedVideoField
from django.template.defaultfilters import slugify

# Create your models here.

USER = get_user_model()


#Tags
SEASON_CHOICES = (
    ('any', 'Any'),
    ('summer', 'Summer'),
    ('winter', 'Winter'),  
)

AVAILABLE_CHOICES = (
    ('select option', 'Select Option'),
    ('inStock', 'In Stock'),
    ('outOfStock', 'Out Of Stock'),
)

SIZE_CHOICES = (
    ('select size', 'Select Size'),
    ('small', 'S'),
    ('medium', 'M'),
    ('large', 'L'),
    ('xlarge', 'Xl'),
    ('xxlarge', 'XXl'),
)

#Category Model

def get_catimage_path(instance, filename):
    if instance.parent:
        parent = instance.parent
        name = instance.title
        return f'{parent}/{name}/images/{filename}'
    else:
        name = instance.title
        return f'{name}/images/{filename}'

class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to=get_catimage_path, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url    

    class MPTTMeta:
        order_insertion_by = ['title'] 

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])       

    def save(self, *args, **kawrgs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        return super().save(*args, **kawrgs)    


#---------------------------------------------------------------------------------------
#Multiple Images for single Product
def get_upload_path(instance, filename):
    name = instance.product.title
    return f'{name}/images/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.product.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        if (image.height > 300 and image.width > 300):
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)


def get_image_path(instance, filename):
    name = instance.title
    return f'{name}/{filename}'

#-------------------------------------------------------------------------------------

#Tag Model
class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)    


#Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length= 100)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    size = models.CharField(choices=SIZE_CHOICES, max_length=11, default='Select Size', blank=True, null=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=get_image_path, blank=True,  null=True)
    video = EmbedVideoField(blank=True)
    discount_price = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    available = models.CharField(choices=AVAILABLE_CHOICES, max_length=20, default='Select Option', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    slug = models.SlugField(max_length=100, unique=True)

    is_namuna_falful = models .BooleanField(default=False)
    supplier = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)

    season_choice = models.CharField(choices=SEASON_CHOICES, max_length=10, default='any')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    

    def __str__(self):     
        return self.title

    @property
    def price_after_discount(self):
        x = self.price - self.discount_price
        return x

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url           
  
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            image = Image.open(self.image.path)
            if (image.height > 300 and image.width > 300):
                output_size = (300, 300)
                image.thumbnail(output_size)
                image.save(self.image.path)
        except:
            url = ''

        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)  


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.product} by {self.name}'


#Product Rating
class Rating(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    
    def __str__(self):
        return f'Rating of product {self.product} by {self.user}'