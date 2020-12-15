from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from .validators import phone_validation

# Create your models here.

USER = get_user_model()


def get_image_path(instance, filename):
    name = instance.username
    return f'{name}/{filename}'

class SupplierProfile(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    about_me = models.TextField()
    shop_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=10, validators=[phone_validation])
    profile_pic = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.user.email

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


waiting_list_status = (
    ('waiting', 'Waiting'),
    ('accept', 'Accept'),
    ('ignore', 'Ignore'),
)

class SupplierForm(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_email = models.EmailField()
    supplier_phone_num = models.CharField(max_length=10, validators=[phone_validation])
    shop_name = models.CharField(max_length=100)
    shop_address = models.CharField(max_length=100)

    status = models.CharField(max_length=10, choices=waiting_list_status, default='waiting')

    def __str__(self):
        return f'Application by {self.shop_name}'

