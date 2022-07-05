from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.views import status

from Users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Testing attributes:
        # email      # done
        # first_name # done
        # last_name  # done
        # password   # done
        # is_seller  # done

        # base testing attributes for product

        cls.email = "gus@email.com"
        cls.first_name = "gus"
        cls.last_name = "tavo"
        cls.password = "123"
        cls.is_seller = True

        cls.user = User.objects.create_user(
            email=cls.email,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
            is_seller=cls.is_seller,
        )

    def test_first_name_exceeds_max_length(self):
        user = User.objects.get(id=1)

        max_length = user._meta.get_field("first_name").max_length

        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)

        max_length = user._meta.get_field("last_name").max_length

        self.assertEquals(max_length, 50)

    def test_seller_true(self):
        self.assertTrue(self.user.is_seller)

    def test_user_has_fields(self):
        self.assertEqual(self.user.email, self.email)

    def test_password_is_hashed(self):
        self.assertNotEqual(self.user.password, self.password)


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        # seller permissions user

        cls.seller_user = dict(
            email="a@a.com",
            first_name="gus",
            last_name="tavo",
            password="123",
            is_seller=True,
        )

        # no permissions user

        cls.regular_user = dict(
            email="b@b.com",
            first_name="gus",
            last_name="tavo",
            password="123",
            is_seller=False,
        )

        cls.super_user = dict(
            email="x@x.com",
            first_name="gus",
            last_name="tavo",
            password="123",
        )

        # key error user

        cls.key_error_user = dict(
            mail="b@b.com",
            first_name="gus",
            last_name="tavo",
            password="123",
            is_seller=False,
        )

        # unactive user

        cls.unactive_user = dict(
            email="b@b.com",
            first_name="gus",
            last_name="tavo",
            password="123",
            is_seller=True,
            is_active=False,
        )

        # seller login user

        cls.seller_login_user = {"email": "a@a.com", "password": "123"}

        # regular login user

        cls.regular_login_user = {"email": "b@b.com", "password": "123"}

        # tokens

    def test_can_create_user_seller(self):
        response = self.client.post("/api/accounts/", self.seller_user)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(self.seller_user["is_seller"], response.data["is_seller"])

    def test_can_create_user_regular(self):
        response = self.client.post("/api/accounts/", self.regular_user)
        self.assertEqual(response.status_code, 201)

        self.assertEqual(self.regular_user["is_seller"], response.data["is_seller"])

    def test_create_wrong_key(self):
        response = self.client.post("/api/accounts/", self.key_error_user)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json()["email"][0], "This field is required.")

    def test_seller_login_generates_token(self):
        user = User.objects.create_user(**self.seller_user)

        response = self.client.post("/api/login/", self.seller_login_user)

        self.assertEqual(user.auth_token.key, response.data["token"])

    def test_regular_login_generates_token(self):
        user = User.objects.create_user(**self.regular_user)

        response = self.client.post("/api/login/", self.regular_login_user)

        self.assertEqual(user.auth_token.key, response.data["token"])

    def test_not_account_owner_patch(self):
        user_1 = User.objects.create_user(**self.regular_user)
        user_2 = User.objects.create_user(**self.seller_user)

        user_1_token = Token.objects.create(user=user_1)

        self.client.credentials(HTTP_AUTHORIZATION="token " + user_1_token.key)

        request_data = {"email": "new@mail.com"}

        response = self.client.patch(f"/api/accounts/{user_2.id}/", request_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_deactivate_user(self):
        regular_user = User.objects.create_user(**self.regular_user)

        regular_user_token = Token.objects.create(user=regular_user)

        self.client.credentials(HTTP_AUTHORIZATION="token " + regular_user_token.key)

        request_data = {"is_active": False}

        response = self.client.patch(
            f"/api/accounts/{regular_user.id}/management/", request_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_activate_user(self):
        unactive_user = User.objects.create_user(**self.unactive_user)
        superuser = User.objects.create_superuser(**self.super_user)

        supertoken = Token.objects.create(user=superuser)

        self.client.credentials(HTTP_AUTHORIZATION="token " + supertoken.key)

        request_data = {"is_active": True}

        response = self.client.patch(
            f"/api/accounts/{unactive_user.id}/management/", request_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_any_user_list_accounts(self):
        user1 = User.objects.create_user(**self.seller_user)
        user2 = User.objects.create_user(**self.regular_user)

        users = [user1, user2]

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(users), len(response.data))
