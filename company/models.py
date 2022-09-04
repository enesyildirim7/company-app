import uuid
from django.db import models
from django_countries.fields import CountryField

def upload_logo(instance,filename):
    return f"company/logo/{filename}"

class Company(models.Model):

    KURULUS_TURU = [
        ("Şahıs","Şahıs"),
        ("Büyük İşletme", "Büyük İşletme"),
        ("KOBİ", "KOBİ"),
        ("STK", "STK"),
    ]

    kurulus_id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="Kuruluş ID")
    kurulus_adi     = models.CharField(max_length=256, verbose_name="Kuruluş Adı")
    kurulus_logo    = models.ImageField(upload_to=upload_logo, verbose_name="Kuruluş Logo", null=True, blank=True)
    kurulus_turu    = models.CharField(max_length=256, choices=KURULUS_TURU, verbose_name="Kuruluş Türü")
    ulke            = CountryField(verbose_name="Ülke")
    website         = models.URLField(max_length=128, verbose_name="Kuruluş Websitesi")
    calisan_sayisi  = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="Kuruluş Çalışan Sayısı")

    def __str__(self):
        return str(self.kurulus_adi)

    class Meta:
        verbose_name = "Şirket"
        verbose_name_plural = "Şirketler"



