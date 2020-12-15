# from .models import SupplierProfile
# from django.conf import settings

# from django.db.models.signals import post_save


# def create_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         supplierprofile = SupplierProfile.objects.create(user=instance)

# post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)


# def save_profile(sender, instance, *args, **kwargs):
#     instance.supplierprofile.save()

# post_save.connect(save_profile, sender=User)    