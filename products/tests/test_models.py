from django.db import IntegrityError
from django.test import TestCase
from ..models import Product
from users.models import User

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.description = "Lorem ipsum dolor1 sit amet, consectetur adipiscing elit. Ut mollis ultrices neque in maximus. Nunc tempus mi risus, ac vestibulum neque ultrices in."
        cls.price =10.00
        cls.quantity = 10
        cls.is_active = True

        cls.user = User.objects.create(
            email="test@mail.com",
            first_name="test", 
            last_name="test",
            is_seller= True
        ) 

        cls.products = [Product.objects.create(description =cls.description,
                price = cls.price,
                quantity = cls.quantity,
                is_active = cls.is_active,seller_id =cls.user  ) for _ in range(20)]

    def test_description(self):
        product = Product.objects.get(id=1)
        self.assertTrue(str(product.description))

    def test_price(self):
        product = Product.objects.get(id=1)
        self.assertTrue(float(product.price))

    def test_quantity(self):
        product = Product.objects.get(id=1)
        self.assertTrue(int(product.quantity))

    def test_is_active(self):
        product = Product.objects.get(id=1)
        self.assertTrue(bool(product.is_active))

    def test_seller_contain_multiple_products(self):
        self.assertEquals(
                len(self.products), 
                self.user.products.count()
            ) 

        for product in self.products:
            self.assertIs(product.seller_id, self.user) 

    def test_product_cannot_belong_to_more_than_one_seller(self):           

        user_two = User.objects.create(
            email="test2@mail.com",
            first_name="test2", 
            last_name="test2",
            is_seller= True
        ) 

        for product in self.products: 
            product.seller_id = user_two
            product.save()

        for product in self.products:
            self.assertNotIn(product, self.user.products.all()) 
            self.assertIn(product, user_two.products.all())

    def test_product_has_information_fields(self):              
        self.assertEqual(self.products[0].description, self.description)
        self.assertEqual(self.products[0].price, self.price)
        self.assertEqual(self.products[0].quantity, self.quantity)
        self.assertEqual(self.products[0].is_active, self.is_active)
        self.assertEqual(self.products[0].seller_id, self.user)


# .isalpha()