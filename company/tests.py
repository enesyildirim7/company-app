from rest_framework.test import APITestCase
from company.models import Company
from users.models import User

class CompanyTestCase(APITestCase):

    def setUp(self):
        """
        Verilerin tanımlanması.
        """

        self.format = "json"

        # Veriler
        self.user_signup = {"email":"test@test.com", "password":"test123", "passcheck":"test123"}
        self.user_login = {"email":"test@test.com", "password":"test123"}

        self.sirketler = [
            {
            "kurulus_adi": "TOGG",
            "kurulus_turu": "Büyük İşletme",
            "ulke": "TR",
            "website": "https://www.togg.com.tr/",
            "calisan_sayisi": "4323"
            },
            {
            "kurulus_adi": "ASELSAN",
            "kurulus_turu": "Büyük İşletme",
            "ulke": "TR",
            "website": "https://www.aselsan.com.tr/",
            "calisan_sayisi": "8888"
            },
            {
            "kurulus_adi": "Google",
            "kurulus_turu": "Büyük İşletme",
            "ulke": "US",
            "website": "https://www.google.com/",
            "calisan_sayisi": "188899"
            },
            {
            "kurulus_adi": "AKUT",
            "kurulus_turu": "STK",
            "ulke": "TR",
            "website": "https://www.akut.org.tr/",
            "calisan_sayisi": "2000"
            },{
            "kurulus_adi": "Özkardeşler San. Tic. Ltd. Şti.",
            "kurulus_turu": "KOBİ",
            "ulke": "TR",
            "website": "https://www.ozkardesler.com/",
            "calisan_sayisi": "26"
            }]

        # Urller
        self.login = "/api/v1/users/login"
        self.signup = "/api/v1/users/signup"
        self.create = "/api/v1/company/create"
        self.list = "/api/v1/company/list"
        self.id = "/api/v1/company/"

        self.filter = lambda kurulus_turu, ulke, calisan_sayisi : f"http://localhost:8000/api/v1/company/list?kurulus_turu={kurulus_turu}&ulke={ulke}&calisan_sayisi={calisan_sayisi}"

        # Signup
        user = User.objects.create(email=self.user_signup["email"])
        user.set_password(self.user_signup["password"])
        user.save()

        # Login
        self.client.post(self.login, self.user_login, format="json")

        return super().setUp()


    def tearDown(self):
        return super().tearDown()

    
    def test_company_create(self):
        """
        Şirket kayıt
        """
        response = self.client.post(self.create, self.sirketler[0], format="json")
        self.assertEqual(response.status_code, 201)


    def test_company_list(self):
        """
        Şirket listesi
        """
        for sirket in self.sirketler:
            self.client.post(self.create, sirket, format="json")

        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    
    def test_get_company_info(self):
        """
        Şirket verileri get metod testi
        """
        sirket = Company.objects.create(
            kurulus_adi=self.sirketler[0]["kurulus_adi"],
            kurulus_turu=self.sirketler[0]["kurulus_turu"],
            ulke=self.sirketler[0]["ulke"],
            website=self.sirketler[0]["website"],
            calisan_sayisi=self.sirketler[0]["calisan_sayisi"]
            )

        response = self.client.get(f"{self.id}{str(sirket.kurulus_id)}", format="json")
        self.assertEqual(response.status_code, 200)


    def test_get_method_invalid_uuid_error(self):
        """
        Get metodu geçersiz UUID hatası
        """
        response = self.client.get(self.id + str("asd"), format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message":"UUID geçerli değil"})



    def test_update_company_data_with_put_method(self):
        """
        Put metodu testi
        """
        sirket = Company.objects.create(
            kurulus_adi=self.sirketler[1]["kurulus_adi"],
            kurulus_turu=self.sirketler[1]["kurulus_turu"],
            ulke="AZ",
            website=self.sirketler[1]["website"],
            calisan_sayisi=1
            )
        response = self.client.put(f"{self.id}{str(sirket.kurulus_id)}", data=self.sirketler[1], format="json")
        self.assertEqual(response.status_code, 201)

        new_data = self.client.get(f"{self.id}{str(sirket.kurulus_id)}", format="json")
        self.assertEqual(response.data, new_data.data)


    def test_put_method_invalid_uuid_error(self):
        """
        Put metodu geçersiz UUID hatası
        """
        
        response = self.client.put(self.id + str("asd"), data=self.sirketler[1], format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message":"UUID geçerli değil"})


    def test_update_company_data_with_patch_method(self):
        """
        Patch metodu testi
        """
        sirket = Company.objects.create(
            kurulus_adi=self.sirketler[2]["kurulus_adi"],
            kurulus_turu=self.sirketler[2]["kurulus_turu"],
            ulke=self.sirketler[2]["ulke"],
            website=self.sirketler[2]["website"],
            calisan_sayisi=self.sirketler[2]["calisan_sayisi"]
            )
        new_calisan_sayisi = 10
        response = self.client.patch(f"{self.id}{str(sirket.kurulus_id)}", data={"calisan_sayisi": new_calisan_sayisi}, format="json")
        self.assertEqual(response.status_code, 201)

        new_data = self.client.get(f"{self.id}{str(sirket.kurulus_id)}", format="json")
        self.assertEqual(new_data.data["calisan_sayisi"], str(new_calisan_sayisi))
    

    def test_patch_method_invalid_uuid_error(self):
        """
        Patch metodu geçersiz UUID hatası
        """
        
        response = self.client.patch(self.id + str("asd"), data={"calisan_sayisi": 10}, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message":"UUID geçerli değil"})
    

    def test_delete_company(self):
        """
        Şirket silme
        """
        sirket = Company.objects.create(
            kurulus_adi=self.sirketler[3]["kurulus_adi"],
            kurulus_turu=self.sirketler[3]["kurulus_turu"],
            ulke=self.sirketler[3]["ulke"],
            website=self.sirketler[3]["website"],
            calisan_sayisi=self.sirketler[3]["calisan_sayisi"]
            )

        response = self.client.delete(f"{self.id}{str(sirket.kurulus_id)}", format="json")
        self.assertEqual(response.status_code, 200)


    def test_error_dueto_non_uuid_while_deleting_company(self):
        """
        Şirket silerken geçersiz UUID hatası
        """
        response = self.client.delete(self.id + "asd", format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message":"UUID geçerli değil"})


    def test_error_dueto_invalid_uuid_while_deleting_company(self):
        """
        Şirket silerken eski id hatası
        """
        response = self.client.delete(self.id + "7b8c9ca0-d5b2-435c-a7d7-d09c9bf7440d", format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"Böyle bir şirket zaten yok."})


    def test_filter_company(self):
        """
        Şirket filtreleme testi
        """

        for sirket in self.sirketler:
            self.client.post(self.create, sirket, format="json")

        kobi_filtre = self.filter(kurulus_turu="KOBİ", ulke="", calisan_sayisi="") # 1 tane var
        stk_filtre = self.filter(kurulus_turu="STK", ulke="", calisan_sayisi="") # 1 tane var
        turkiye_filtre = self.filter(kurulus_turu="", ulke="TR", calisan_sayisi="") # 4 tane var
        abd_filtre = self.filter(kurulus_turu="", ulke="US", calisan_sayisi="") # 1 tane var 
        buyuk_isletme = self.filter(kurulus_turu="Büyük İşletme", ulke="", calisan_sayisi="") # 3 tane var

        kobi_response = self.client.get(kobi_filtre, format="json")
        self.assertEqual(kobi_response.status_code, 200)
        self.assertEqual(len(kobi_response.data), 1)

        stk_response = self.client.get(stk_filtre, format="json")
        self.assertEqual(stk_response.status_code, 200)
        self.assertEqual(len(stk_response.data), 1)

        turkiye_response = self.client.get(turkiye_filtre, format="json")
        self.assertEqual(turkiye_response.status_code, 200)
        self.assertEqual(len(turkiye_response.data), 4)

        abd_response = self.client.get(abd_filtre, format="json")
        self.assertEqual(abd_response.status_code, 200)
        self.assertEqual(len(abd_response.data), 1)

        buyuk_response = self.client.get(buyuk_isletme, format="json") 
        self.assertEqual(buyuk_response.status_code, 200)
        self.assertEqual(len(buyuk_response.data), 3)



        

        



