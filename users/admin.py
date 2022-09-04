from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    isim        = forms.CharField(max_length=128, label="İsim")
    soyisim     = forms.CharField(max_length=128, label="Soyisim")
    email       = forms.EmailField(label="Email")
    password    = forms.CharField(max_length=128, label="Şifre")
    passcheck   = forms.CharField(max_length=128, label="Şifre tekrar")

    class Meta:
        model = User
        fields = ('isim','soyisim','email','password','passcheck')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        passcheck = self.cleaned_data.get('passcheck')

        if (password and passcheck) and (password != passcheck):
            raise ValidationError("Parolalar eşleşmiyor. Doğru yazdığından emin ol.")

        return passcheck
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('isim','soyisim','email','password')

class CustomUserAdmin(UserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('isim','soyisim','email','uyelik_tarihi','son_giris','is_admin','is_active','is_staff','is_superuser')
    list_filter = ('is_admin','is_active','is_staff','is_superuser')
    readonly_fields = ('uyelik_tarihi','son_giris')

    fieldsets = (
        (
            None, {
                "fields": (
                    'isim','soyisim','email','takip'
                    )
            }),
            
            ("Giriş Kayıtları", {"fields": ('uyelik_tarihi','son_giris'),},),
            ("Yetkiler", {"fields": ('is_active','is_admin','is_superuser','is_staff','groups','user_permissions'),},),
        )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('isim','soyisim','email','password','passcheck','takip','uyelik_tarihi','son_giris')
        }),
    )
    search_fieldsets = ('isim','soyisim','email')
    ordering = ('email',)
    filter_horizontal = ()
    
admin.site.register(User, CustomUserAdmin)
