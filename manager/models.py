from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
from PIL import Image
from seller.validators import phone_validation

# Create your models here.

USER = get_user_model()

def get_image_path(instance, filename):
    name = instance.username
    return f'manager/{name}/{filename}'


class Manager(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=10, validators=[phone_validation])
    profile_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.user.email

    @property
    def calculate_age(self):
        age = date.today().year - self.dob.year 
        return age 

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try: 
            image = Image.open(self.profile_pic.path)
            if (image.height>300 and image.width>300):
                output_size = (300, 300)
                image.thumbnail(output_size)
                image.save(self.profile_pic.path)  
        except:
            url = ''  


#Model for Home Main Slider 
def get_slider_path(instance, filename):
    name = instance.title
    return f'home_main_slider/{name}/{filename}'

class HomeTopSlider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_slider_path)
    detail = models.TextField()

    def __str__(self):
        return f'Slider of {self.title}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url    


#Model for Our Products Are Section 
def get_product_info_path(instance, filename):
    name = instance.info
    return f'our_product_are/{name}/{filename}'

class OurProductsAre(models.Model):
    image = models.ImageField(upload_to=get_product_info_path)
    info = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.info}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url