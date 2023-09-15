from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

# doğru veriler ile kayıt işlemi yap.
# şifre invalid olabilir.
# kullanıcı adı kullanılmış olabilir.
# üye girişi yaptıysak o sayfa gözükmemeli
# token ile giriş işlemi yapıldığında 403 hatası
from rest_framework.utils import json


#bu işlmelerin aynısını postman veya drf kendi test browserdan yapıp ne dondugune bakmamı lazım buda onların harici kod ile yapıyor
#testi neye gore yazcaz sayfya manuel girip onları ayaynısını yazıcaz aslında
class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")
    def test_user_registration(self):
        """
            Register with happy path
        """

        data = {
            "username" : "admin",
            "password": "admin123"
        }

        # istek de bir response birde status code donecek
        # dogur veriler ile 201 donleli donerse testi gectik
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        """
            invalid password verisi ile kayıt işlemi.
        """

        data = {
            "username" : "admin",
            "password": "1"
        }

        # invalidde 400 donmeli donerse testi gectik
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        """
            Unique username test
        """
        self.test_user_registration()
        data = {
            "username" : "admin",
            "password": "dsfdf34"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """
            session ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()
        self.client.login(username = 'admin', password = 'admin123')
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)


    #bunları ilk yazıyoruz bunlar clietn tarafındada yapılcak aslında ilk burdan yazıyoruz ne yapcagımız zten belli
    #tokendan bas gec direk
    def test_user_authenticated_token_registration(self):
        """
            token ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()

        data = {
            "username": "admin",
            "password": "admin123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200 , response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ token)
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)


#Testleri class yanndaki yesil buton ile icindeki butun methodları calıstırırız
#sınır koymustuk too many request 429 donerblir bu saatte erisim hakkı ile ilgil donen bir hata
class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):  # setup kendi metodu contructor gibi ilk bu calısıyor class calıstıgında testler calısmadan once calısan metod
        self.username = "admin"
        self.password = "pass123"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login, {"username": "admin", "password": "alala123"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):  # git safadan bak yanlıs bilgilerle ne donuyor sonra buraya kodu yaz
        response = self.client.post(self.url_login, {"username": "asasdzxczxc", "password": "sifre1234"})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):  # 400 bad request alırız boş bilgilerle giris yapmısmıyız
        response = self.client.post(self.url_login, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)


class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse("token_obtain_pair")
    def setUp(self):
        self.username = "admin"
        self.password = "adminnewpass"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username" : "admin",
            "password" : "adminnewpass"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # oturum açılmadan girildiğinde hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "old_password": "sifre1234",
            "new_password": "asdasdas123456"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_informations(self):
        self.login_with_token()
        data = {
            "old_password": "asdasd",
            "new_password": "asdasdas123456"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_with_empty_informations(self):
        self.login_with_token()
        data = {
            "old_password": "",
            "new_password": ""
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)

class UserProfileUpdate(APITestCase):
    url = reverse("accounts:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "admin"
        self.password = "sifre1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username": "admin",
            "password": "sifre1234"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # oturum açılmadan girildiğinde hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
    # valid informations
    def test_with_valid_informations(self):
        self.login_with_token()
        # content bak sayfadan aynısnı yazıyoruz
        data = {
            "id": 1,
            "first_name": "sdad",
            "last_name": "sdsda",
            "profile": {
                "id": 1,
                "about": "note",
                "twitter": "asdas"
            }
        }

        response = self.client.put(self.url, data,
                                   format='json')  # ocnekilerde json formatında sonunda tabi ama tam dgldi bnda ama ytam json gnderiyorz
        self.assertEqual(200, response.status_code)
        print(response.data)
        print(json.loads(response.content))
        self.assertEqual(json.loads(response.content), data)  # serverdan gelen bilgi gondeiln bilgileryimtdi

    def test_with_empty_informations(self):
        self.login_with_token()
        data = {
            "id": 1,
            "first_name": "",
            "last_name": "",
            "profile": {
                "id": 1,
                "note": "",
                "twitter": ""
            }
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(200, response.status_code)
# BURALARDA ID HEP BIR CNKU TESTI CALISTIGINDA TEST DB SINDE SADECE 1 ID LI BIRSEY OLACAK SECUENCE OLAYI OLMAYACAK
# TESTTE 2 TANE USER OLSA IDI ONLARA MUDAHALE OLURDU


# from django.contrib.auth.models import User
# from django.test import TestCase
# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework.utils import json
#
#
# #dgru verileri ile kayt yap
# #sifre invalid olablr
# #username var olablr
# #uye girisi yptysak o sayfa gozukmemeli forbidden olayı
# #token islemi yaptysak gozukmemeli 403 haası
#
# ## uye igiris ypnca session oluyor ama token istegiden tokenla giris oluyor 2 turu var
#
# class UserRegistrationTestCase(APITestCase):
#     url = reverse("user:register")
#     url_login = reverse("token_obtain_pair")
#
#     def test_user_registration(self):   # yanndaki run a tkla
#         """
#         Dogru verileri ile kayit
#         """
#         data = {
#             "username" : "mustafatest12asd",
#             "password" : "deneme123"
#         }
#
#         response = self.client.post(self.url, data)    #client gibi davranmasini sglar
#         self.assertEqual(201, response.status_code)
#         #201 createed edildigini kod ise bsey dnblr, doner status kod 201 ise test passed
#         #status kod 201 esitse demek esitse testi gec
#
#     def test_user_invalid_password(self):
#         """
#         invalid password verisi ile kayit
#         """
#         data = {
#             "username": "mustafatest12asd",
#             "password": "1"
#         }
#
#         response = self.client.post(self.url, data)
#         self.assertEqual(400, response.status_code)  #400 dnmeli brada istedigimiz 400
#
#     def test_user_unique_name(self):
#         """
#         benzersz isim testi
#         """
#         self.test_user_registration()
#         data = {
#             "username": "mustafatest12asd",
#             "password": "deneme123"
#         }
#
#         response = self.client.post(self.url, data)
#         self.assertEqual(400, response.status_code)  #400 dnmeli brada istedigimiz 400
#
#     def test_user_authenticated_registration(self):
#         """
#         session ile giris yapmıs bu sayfayi gorememeli
#         """
#         self.test_user_registration()  # uye olustur
#
#         self.client.login(username = "mustafatest12asd", password = 'deneme123') #uye giris yap
#         response = self.client.get(self.url)
#         self.assertEqual(403, response.status_code)  #400 dnmeli brada istedigimiz 400
#
#     def test_user_authenticated_token_registration(self):
#         """
#             token ile giriş yapmış kullanıcı sayfayı görememeli.
#         """
#         self.test_user_registration()
#
#         data = {
#             "username": "mustafatest12asd",
#             "password": "deneme123"
#         }
#         response = self.client.post(self.url_login, data)
#         self.assertEqual(200 , response.status_code)
#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ token) # clienttanda byle grcez
#         response_2 = self.client.get(self.url)
#         self.assertEqual(403, response_2.status_code)
#
#
# class UserLogin(APITestCase):
#     url_login = reverse("token_obtain_pair")
#
#     def setUp(self):  # constructor gibi bu isleyecek bu kod
#         self.username = "admin "
#         self.password = "alala123"
#         self.user = User.objects.create_user(username = self.username, password=self.password)
#
#     def test_user_token(self):
#          response = self.client.post(self.url_login, {"username": "admin", "password":"alala123"})
#          self.assertEqual(200, response.status_code)
#          print(json.loads(response.content))
#          self.assertTrue("access" in json.loads(response.content))  # donen icinde access varmı
#
#     def test_user_invalid_data(self):
#          response = self.client.post(self.url_login, {"username": "asasdzxczxc", "password":"sifre1234"})
#          self.assertEqual(401, response.status_code)  #sallma blgilerle 401 dnermi kullanıcı olmadgnda dnen deger
#
#     def test_user_empty_data(self):
#          response = self.client.post(self.url_login, {"username": "", "password":""})
#          self.assertEqual(400, response.status_code)  # empty data bad request olur 400 dnmeli
#
#
# class UserPasswordChange(APITestCase):
#     url = reverse("user:change-password")
#     url_login = reverse("token_obtain_pair")
#     def setUp(self):
#         self.username = "oguzhan"
#         self.password = "sifre1234"
#         self.user = User.objects.create_user(username = self.username, password=self.password)
#
#     def login_with_token(self):
#         data = {
#             "username" : "oguzhan",
#             "password" : "sifre1234"
#         }
#         response = self.client.post(self.url_login, data)
#         self.assertEqual(200, response.status_code)
#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#
#     # oturum açılmadan girildiğinde hata
#     def test_is_authenticated_user(self):
#         response = self.client.get(self.url)
#         self.assertEqual(401, response.status_code)
#
#
#     def test_with_valid_informations(self):
#         self.login_with_token()
#         data = {
#             "old_password": "sifre1234",
#             "new_password": "asdasdas123456"
#         }
#         response = self.client.put(self.url, data)
#         self.assertEqual(204, response.status_code)
#
#     def test_with_wrong_informations(self):
#         self.login_with_token()
#         data = {
#             "old_password": "asdasd",
#             "new_password": "asdasdas123456"
#         }
#         response = self.client.put(self.url, data)
#         self.assertEqual(400, response.status_code)
#
#     def test_with_empty_informations(self):
#         self.login_with_token()
#         data = {
#             "old_password": "",
#             "new_password": ""
#         }
#         response = self.client.put(self.url, data)
#         self.assertEqual(400, response.status_code)
#
# class UserProfileUpdate(APITestCase):
#     url = reverse("user:me")
#     url_login = reverse("token_obtain_pair")
#
#     def setUp(self):
#         self.username = "oguzhan"
#         self.password = "sifre1234"
#         self.user = User.objects.create_user(username=self.username, password=self.password)
#
#     def login_with_token(self):
#         data = {
#             "username": "oguzhan",
#             "password": "sifre1234"
#         }
#         response = self.client.post(self.url_login, data)
#         self.assertEqual(200, response.status_code)
#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#
#     # oturum açılmadan girildiğinde hata
#     def test_is_authenticated_user(self):
#         response = self.client.get(self.url)
#         self.assertEqual(401, response.status_code)
#     # valid informations
#     def test_with_valid_informations(self):
#         self.login_with_token()
#         data = {
#             "id" : 1,
#             "first_name": "",
#             "last_name": "",
#             "profile": {
#                 "id": 1,
#                 "note": "",
#                 "twitter": "asdas"
#             }
#         }
#
#         response = self.client.put(self.url, data, format = 'json')
#         self.assertEqual(200, response.status_code)
#         print(response.data)
#         print(response.content)  #farklari birinde ordered_dict geliyor data yapısı braz farklı
#         print(json.loads(response.content))
#         self.assertEqual(json.loads(response.content), data)  #sunucudan gnderlien bzm gnergimizimi
#
#     def test_with_empty_informations(self):
#         self.login_with_token()
#         #ornek db olstruyluyor yeni user olstr otomatk profile olsuyuro onn prfile id side 1 oluyor
#         data = {
#             "id": 1,
#             "first_name": "",
#             "last_name": "",
#             "profile": {
#                 "id": 1,
#                 "note": "",
#                 "twitter": ""
#             }
#         }
#         response = self.client.put(self.url, data, format='json')  #json tipinde gnderiyoruz
#         self.assertEqual(200, response.status_code)
