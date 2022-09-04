from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "isim", "soyisim", "email", "password", "takip", "uyelik_tarihi", "son_giris", "is_admin", "is_active", "is_staff", "is_superuser"]

        def create(self, validated_data):
            password = validated_data.pop('password')
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance