from django.db import models
from django.contrib.auth import get_user_model
from seller.validators import phone_validation
from datetime import date
from PIL import Image

# Create your models here.

USER = get_user_model()


def get_image_path(instance, filename):
    name = instance.username
    return f'{name}/{filename}'

class CustomerProfile(models.Model):
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
            if (image.height > 300 and image.width > 300):
                output_size = (300, 300)
                image.thumbnail(output_size)
                image.save(self.profile_pic.path)     
        except:
            url = ''