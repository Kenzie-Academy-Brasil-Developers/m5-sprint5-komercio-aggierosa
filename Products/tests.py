from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Products.models import Product
from Users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Testing attributes:
        # descripton # done
        # price      # done
        # quantity   # done
        # is_active  # done
        # is_seller  # done

        # base testing attributes for product

        cls.descripton = "produto"
        cls.price = 1.5
        cls.quantity = 1
        cls.is_active = True

        #  multiple products test

        cls.seller = User.objects.create(
            email="a@a.com",
            first_name="a",
            last_name="a",
            password="1234",
            is_seller=True,
        )

        cls.products = [
            Product.objects.create(
                descripton=cls.descripton,
                price=cls.price,
                quantity=cls.quantity,
                is_active=cls.is_active,
                seller_id=1,
            )
            for _ in range(19)
        ]

        # individual product test

        cls.test_seller = User.objects.create(
            email="b@b.com",
            first_name="b",
            last_name="b",
            password="1234",
            is_seller=True,
        )
        cls.test_product = Product.objects.create(
            descripton=cls.descripton,
            price=cls.price,
            quantity=cls.quantity,
            is_active=cls.is_active,
            seller_id=2,
        )

    def test_price_exceeds_max_digits(self):
        product = Product.objects.get(id=1)

        max_digits = product._meta.get_field("price").max_digits

        self.assertEquals(max_digits, 8)

    def test_seller_may_contain_multiple_products(self):
        self.assertEquals(len(self.products), self.seller.products.count())

        for product in self.products:
            self.assertEqual(product.seller, self.seller)

    def test_product_is_active(self):
        self.assertIs(self.test_product.is_active, True)

    def test_has_field(self):
        self.assertEqual(self.test_product.descripton, self.descripton)

    def test_quantity_is_positive(self):
        minimum = 0

        self.assertGreater(self.test_product.quantity, minimum)


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.seller = User.objects.create(
            email="a@a.com",
            first_name="gus",
            last_name="tavo",
            password="123",
            is_seller=True,
        )

        cls.seller_token = Token.objects.create(user=cls.seller)

        # base product

        cls.product = dict(
            descripton="produto",
            price=1.5,
            quantity=1,
            is_active=True,
            seller_id=cls.seller.id,
        )

        # wrong key product

        cls.wrong_key_product = dict(
            descripton="produto",
            ice=1.5,
            quantity=1,
            is_active=True,
            seller_id=cls.seller.id,
        )

        # negative quantity product

        cls.negative_quantity = dict(
            descripton="produto",
            price=1.5,
            quantity=-1,
            is_active=True,
            seller_id=cls.seller.id,
        )

    def test_seller_creates_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="token " + self.seller_token.key)

        response = self.client.post("/api/products/", self.product)

        self.assertEqual(response.status_code, 201)

    def test_seller_updates_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="token " + self.seller_token.key)

        response = self.client.post("/api/products/", self.product)

        request_patch = dict(description="produto atualizado")

        response = self.client.patch("/api/products/1/", request_patch)

        self.assertEqual(response.status_code, 200)

    def test_regular_list_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)

    def test_regular_filter_products(self):
        product_sample = Product.objects.create(**self.product)

        response = self.client.get(f"/api/products/{product_sample.id}/")

        self.assertEqual(response.status_code, 200)

    def test_serializer_list_differ_create(self):
        response_create = self.client.post("/api/products/", self.product)

        response_list = self.client.get("/api/products/")

        self.assertNotEqual(response_create, response_list)

    def test_wrong_key(self):
        self.client.credentials(HTTP_AUTHORIZATION="token " + self.seller_token.key)

        response = self.client.post("/api/products/", self.wrong_key_product)

        self.assertIn("price", response.data)
        self.assertIn(response.data["price"][0].code, "required")

    def test_create_product_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION="token " + self.seller_token.key)

        response = self.client.post("/api/products/", self.negative_quantity)

        self.assertIn(response.data["quantity"][0].code, "min_value")
