from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["kurulus_id","kurulus_adi","kurulus_logo","kurulus_turu","ulke","website","calisan_sayisi"]
