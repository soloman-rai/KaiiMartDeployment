from django.db import models

from django.contrib.auth import get_user_model
from product.models import Category
from PIL import Image

# Create your models here.

USER = get_user_model()


def get_upload_path(instance, filename):
    name = instance.post_title
    return f'{name}/images/{filename}'

class BlogModel(models.Model):
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    post_title = models.CharField(max_length=150)
    post_text = models.TextField()
    image = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post_title}, {self.author}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    


class BlogComment(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.blog} by {self.name}'
