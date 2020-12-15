# from .models import CustomerProfile
# from django.conf import settings

# from django.db.models.signals import post_save


# def create_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         customerprofile = CustomerProfile.objects.create(user=instance)

# post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
