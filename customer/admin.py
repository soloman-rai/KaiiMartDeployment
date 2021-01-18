from django.contrib import admin
from .models import CustomerProfile, NewsletterSubscription, Enquiry

# Register your models here.

admin.site.register(CustomerProfile)
admin.site.register(NewsletterSubscription)
admin.site.register(Enquiry)