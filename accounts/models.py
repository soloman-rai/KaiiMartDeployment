from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.utils.timezone import now

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have email address")
        if not password:
            raise ValueError("Users must have a password")
        
        user_obj = self.model(email=self.normalize_email(email),
                                username=username)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username=None, password=None):
        user = self.create_user(email, username=username,
                                password=password, is_staff=True)
        return user   

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(email, username=username,
                                password=password, is_staff=True, is_admin=True)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_customer = models.BooleanField(default=False, verbose_name='Customer')
    is_supplier = models.BooleanField(default=False, verbose_name='Supplier')
    is_delivery_team = models.BooleanField(default=False, verbose_name='DeliveryTeam')
    is_manager = models.BooleanField(default=False, verbose_name='Manager')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Active', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff                

    @property
    def is_admin(self):
        return self.admin
