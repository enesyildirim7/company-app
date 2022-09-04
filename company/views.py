from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import *
from django_filters import filters, FilterSet
from django_countries import countries
from rest_framework.generics import *
from rest_framework import status
from .serializer import *
from .models import *

PERMISSION = IsAuthenticated

class CompanyFilter(FilterSet):
    """
    Kuruluşu türüne, ülkesine ve çalışan sayısına göre filtreler.
    Filtreleme:
    Kuruluş türü = ["Şahıs", "KOBİ", "Büyük İşletme", "STK"]
    Ülke = Django country kütüphanesi ülke verileri.
    Çalışan sayısı = Girilen değerden eşit veya daha küçük.
    """

    kurulus_turu = ChoiceFilter(choices=Company.KURULUS_TURU)
    ulke = ChoiceFilter(choices=countries)
    calisan_sayisi = NumberFilter(field_name="calisan_sayisi", lookup_expr="lte")
    class Meta: 
        model: Company
        fields = ["kurulus_turu","ulke","calisan_sayisi"]


class CompanyListView(ListAPIView):
    """
    Bütün şirketleri döndürür.
    Kuruluş türü, ülke ve çalışan sayısına göre filtreleme imkanı sunar.
    """
    
    permission_classes = [PERMISSION]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kurulus_turu","ulke","calisan_sayisi"]
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    queryset = Company.objects.all()


class CompanyCreateView(CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [PERMISSION]
    # parser_classes = [MultiPartParser, FormParser] #TODO: production

    def post(self, request, format=None):
        """
        Şirket kaydı.
        """

        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyCRUDView(APIView):
    serializer_class = CompanySerializer
    permission_classes = [PERMISSION]
    lookup_field = "kurulus_id"

    def get(self, request, kurulus_id, format=None):
        """
        Bütün şirketlerin listesini döndürür.
        """
        try:
            id = UUID(kurulus_id, version=4)
            sirket = Company.objects.filter(kurulus_id=kurulus_id)
            if sirket.exists():
                serializer = CompanySerializer(sirket, many=True).data[0]
                return Response(serializer, status=status.HTTP_200_OK)
            return Response({"message":"Kayıtlı değil."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"UUID geçerli değil"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, kurulus_id, format=None):
        """
        Şirket verilerini günceller.
        """
        try:
            id = UUID(kurulus_id, version=4)

            sirket = Company.objects.filter(kurulus_id=kurulus_id).first()
            serializer = CompanySerializer(sirket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"UUID geçerli değil"}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, kurulus_id, format=None):
        """
        Sadece gönderilen şirket verilerini günceller.
        """
        try:
            id = UUID(kurulus_id, version=4)

            sirket = Company.objects.filter(kurulus_id=kurulus_id).first()
            serializer = CompanySerializer(sirket, data=request.data ,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"UUID geçerli değil"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, kurulus_id, format=None):
        """
        Şirketi siler.
        """
        try:
            id = UUID(kurulus_id, version=4)

            sirket = Company.objects.filter(kurulus_id=kurulus_id)
            if sirket.exists():
                sirket.delete()
                return Response({"message":"Şirket silindi."},status=status.HTTP_200_OK)
            return Response({"message":"Böyle bir şirket zaten yok."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"UUID geçerli değil"}, status=status.HTTP_404_NOT_FOUND)