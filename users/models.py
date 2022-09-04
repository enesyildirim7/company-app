import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from company.models import *


class UserManager(BaseUserManager):

    def create_user(self, isim, soyisim, email, password=None):
        if not email:
            raise ValueError("Email adresinizi girin.")

        if not password:
            raise ValueError("Şifrenizi girin.")
        
        email = self.normalize_email(email)

        user = self.model(isim=isim, soyisim=soyisim, email=email)

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, isim, soyisim, email, password=None):

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_admin(self, isim, soyisim, email, password=None):

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_staff(self, isim, soyisim, email, password=None):

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, password=password)

        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="Kullanıcı ID")
    isim            = models.CharField(max_length=128, verbose_name='İsim', unique=False, blank=True, null=True)
    soyisim         = models.CharField(max_length=128, verbose_name='Soyisim', unique=False, blank=True, null=True)
    email           = models.EmailField(max_length=128, verbose_name='Email', unique=True)
    password        = models.CharField(max_length=128, verbose_name='Şifre', unique=False)
    takip           = models.ManyToManyField(Company, verbose_name="Takip Edilen Şirketler", blank=True)
    uyelik_tarihi   = models.DateTimeField(auto_now_add=True ,verbose_name="Üyelik Tarihi")
    son_giris       = models.DateTimeField(auto_now=True, verbose_name="Son Oturum")
    is_admin        = models.BooleanField(default=False, verbose_name="Yönetici")
    is_active       = models.BooleanField(default=True, verbose_name="Aktif Hesap")
    is_staff        = models.BooleanField(default=False, verbose_name="Personel")
    is_superuser    = models.BooleanField(default=False, verbose_name="Genel Yönetici")

    EMAIL_FIELD     = "email"
    USERNAME_FIELD  = "email"

    objects = UserManager()

    def __str__(self):
        return str(self.isim)

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"