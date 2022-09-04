from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from rest_framework.generics import *
from rest_framework import status
from company.models import *
from company.serializer import *
from .serializer import *
from .models import *

PERMISSION = AllowAny

class UserSignupView(APIView):
    permission_classes = [PERMISSION]

    def post(self, request, format=None):
        if request.data:
            data = request.data
            email = data["email"]
            password = data["password"]
            passcheck = data["passcheck"]

        try:
            if password == passcheck:
                if User.objects.filter(email=email).exists():
                    return Response({"message": "Mail adresi zaten var."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if len(password) < 5:
                        return Response({"message": "Parola en az 5 karakterli olmalı."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data.pop("passcheck")
                        user = UserSerializer(data=data)
                        if user.is_valid():
                            user.save()
                            return Response({"message": "Kullanıcı başarıyla oluşturuldu."}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message": "Kullanıcı oluşturulamadı."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Parolalar eşleşmiyor. Doğru yazdığından emin ol."}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"message": "Hata oluştu."}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(APIView):
    permission_classes = [PERMISSION]
    
    def post(self, request, format=None):
        if request.data["email"] and request.data["password"]:
            data = request.data
            email = data["email"]
            password = data["password"]
        else:
            return Response({"message": "Lütfen kullanıcı adı ve parolanızı yazın."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if request.user.is_authenticated:
                return Response({"message": "Oturum zaten açık."},status=status.HTTP_200_OK)

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Giriş yapıldı!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Kimlik doğrulama hatası."}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response({"message": "Kimlik doğrulanırken bir şeyler ters gitti."}, status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            if not request.user.is_authenticated:
                return Response({"message": "Oturum zaten kapalı."}, status=status.HTTP_308_PERMANENT_REDIRECT)
            else:
                logout(request)
                return Response({"message": "Çıkış yapıldı!"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Çıkış yapılamadı."}, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = UserSerializer(request.user).data
        return Response({"user": user}, status=status.HTTP_200_OK)


class CompanyFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Takip edilen şirketleri listeler.
        """
        try:

            USER_ID = request.user.id
            user = User.objects.prefetch_related("takip").filter(id=USER_ID).first()
            takip = user.takip.all()
            serializer = CompanySerializer(takip, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Bir şeyler ters gitti."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """
        Şirketi takip edilenlere ekler.
        """

        try:
            USER_ID = request.user.id
            KURULUS_ID = request.data["kurulus_id"]
            sirket = Company.objects.get(kurulus_id=KURULUS_ID)
            user = User.objects.get(id=USER_ID)
            if user.takip.filter(kurulus_id=KURULUS_ID).exists():
                return Response({"message": f"{sirket.kurulus_adi} zaten takip ediliyor."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.takip.add(sirket)
                return Response({"message": f"{sirket.kurulus_adi} takip edilmeye başlandı."}, status=status.HTTP_200_OK)
        except:
            return Response({"message":"Bir şeyler ters gitti."},status=status.HTTP_400_BAD_REQUEST)