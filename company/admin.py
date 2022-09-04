from django.contrib import admin
from .models import *

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('kurulus_adi','kurulus_turu','ulke','website','calisan_sayisi')

admin.site.register(Company, CompanyAdmin)
