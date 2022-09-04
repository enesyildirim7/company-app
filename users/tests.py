from rest_framework.test import APITestCase
from company.models import Company
from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        """
        Verilerin tanımlanması.
        """
        
        self.user_signup = {"email":"test@test.com", "password":"test123", "passcheck":"test123"}
        self.user_login = {"email":"test@test.com", "password":"test123"}

        self.sirketler = [{
            "kurulus_adi": "TOGG",
            "kurulus_logo": "/media/company/logo/togg.jpg",
            "kurulus_turu": "Büyük İşletme",
            "ulke": "TR",
            "website": "https://www.togg.com.tr/",
            "calisan_sayisi": "4323"
            },
            {
            "kurulus_adi": "ASELSAN",
            "kurulus_logo": "/media/company/logo/aselsan.png",
            "kurulus_turu": "Büyük İşletme",
            "ulke": "TR",
            "website": "https://www.aselsan.com.tr/",
            "calisan_sayisi": "8888"
            }]

        self.signup = "/api/v1/users/signup"
        self.login = "/api/v1/users/login"
        self.logout = "/api/v1/users/logout"
        self.me = "/api/v1/users/me"
        self.follow = "/api/v1/users/follow"

        return super().setUp()


    def tearDown(self):
        return super().tearDown()


    def test_user_signup(self):
        """
        Kullanıcı kayıt testi.
        """

        res = self.client.post(self.signup, self.user_signup, "json")
        self.assertEqual(res.status_code, 201)


    def test_user_login(self):
        """
        Kullanıcı giriş testi.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        response = self.client.post(self.login, self.user_login, "json")
        self.assertEqual(response.status_code, 201)


    def test_user_signup_email_already_exist(self):
        """
        Kayıtlı email hata.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()
        response = self.client.post(self.signup, self.user_signup, "json")
        self.assertEqual(response.status_code, 400)


    def test_user_signup_password_length(self):
        """
        Şifre uzunluk kontrolü.
        """
        response = self.client.post(self.signup, data={"email":self.user_signup["email"], "password":"123" ,"passcheck":"123"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": "Parola en az 5 karakterli olmalı."})

    def test_user_signup_password__doesnt_match(self):
        """
        Şifre kontrolü eşleşmiyor.
        """
        response = self.client.post(self.signup, data={"email":self.user_signup["email"], "password":"asdasd" ,"passcheck":"123456"}, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"message": "Parolalar eşleşmiyor. Doğru yazdığından emin ol."})


    def test_user_already_logged_in(self):
        """
        Giriş yapmış kullanıcı tekrar giriş yapma testi.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, self.user_login, "json")

        response = self.client.post(self.login, self.user_login, "json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, {"message":"Oturum zaten açık."})


    def test_user_login_with_invalid_email_password(self):
        """
        Kullanıcı eksik veri ile giriş testi.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        response = self.client.post(self.login, {"email":"","password":"test123"}, "json")
        self.assertEqual(response.status_code, 400)


    def test_user_login_error(self):
        """
        Kayıtsız kullanıcı kimlik doğrulama hatası testi.
        """
        response = self.client.post(self.login, self.user_login, "json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data,{"message": "Kimlik doğrulama hatası."})

        
    def test_user_info(self):
        """
        Kullanıcı bilgileri alma testi.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, data=self.user_login, format="json")
        response = self.client.get(self.me, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["email"], self.user_signup["email"])


    def test_user_follow_get(self):
        """
        Kullanıcının takip ettiği kuruluşlar.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, data=self.user_login, format="json")

        for sirket in self.sirketler:
            Company.objects.create(
                kurulus_adi=sirket["kurulus_adi"],
                kurulus_logo=sirket["kurulus_logo"],
                kurulus_turu=sirket["kurulus_turu"],
                ulke=sirket["ulke"],
                website=sirket["website"],
                calisan_sayisi=sirket["calisan_sayisi"]
                )
        takip_sirket = Company.objects.get(kurulus_adi="ASELSAN")
        user.takip.add(takip_sirket)

        response = self.client.get(self.follow, format="json")
        self.assertEqual(response.status_code, 200)


    def test_user_follow_post(self):
        """
        Kullanıcı kuruluş takip etme.
        """
        
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, data=self.user_login, format="json")

        for sirket in self.sirketler:
            Company.objects.create(
                kurulus_adi=sirket["kurulus_adi"],
                kurulus_logo=sirket["kurulus_logo"],
                kurulus_turu=sirket["kurulus_turu"],
                ulke=sirket["ulke"],
                website=sirket["website"],
                calisan_sayisi=sirket["calisan_sayisi"]
                )
        takip_sirket = Company.objects.get(kurulus_adi="ASELSAN")
        
        response = self.client.post(self.follow, data={"kurulus_id":takip_sirket.kurulus_id}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": f"{takip_sirket.kurulus_adi} takip edilmeye başlandı."})


    def test_user_follow_already_followed_company(self):
        """
        Zaten takip edilen şirketi tekrar takip etme hatası.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, data=self.user_login, format="json")

        for sirket in self.sirketler:
            Company.objects.create(
                kurulus_adi=sirket["kurulus_adi"],
                kurulus_logo=sirket["kurulus_logo"],
                kurulus_turu=sirket["kurulus_turu"],
                ulke=sirket["ulke"],
                website=sirket["website"],
                calisan_sayisi=sirket["calisan_sayisi"]
                )
        takip_sirket = Company.objects.get(kurulus_adi="ASELSAN")
        
        self.client.post(self.follow, data={"kurulus_id":takip_sirket.kurulus_id}, format="json") # İlk takip

        response = self.client.post(self.follow, data={"kurulus_id":takip_sirket.kurulus_id}, format="json") # İkinci takip
        self.assertEqual(response.status_code, 400)


    def test_user_logout(self):
        """
        Kullanıcı çıkış.
        """
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        self.client.post(self.login, data=self.user_login, format="json")

        response = self.client.post(self.logout, format="json")
        self.assertEqual(response.status_code, 200)