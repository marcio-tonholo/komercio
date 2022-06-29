from django.db import IntegrityError
from django.test import TestCase
from ..models import User
import re

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "teste@mail.com"
        cls.first_name = "test"
        cls.last_name = "test"
        cls.is_seller = True

        cls.user = User.objects.create(
            email=cls.email,
            first_name=cls.first_name, 
            last_name=cls.last_name,
            is_seller= cls.is_seller
        ) 

    def test_email(self):
            user = User.objects.get(id=1)
            max_length = user._meta.get_field('email').max_length
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            self.assertTrue(re.fullmatch(regex, user.email))
            
            self.assertEquals(max_length, 255)
            
            with self.assertRaises(IntegrityError):
                User.objects.create(
                email=self.email,
                first_name=self.first_name, 
                last_name=self.last_name,
                is_seller= self.is_seller
            ) 

    def test_first_name(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_username(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEquals(max_length, 255)
        self.assertIsNone(user.username)

    def test_is_seller(self):
        user = User.objects.get(id=1)
        self.assertTrue(bool(user.is_seller))

    def test_user_has_information_fields(self):              
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.is_seller, self.is_seller)
        self.assertIsNone(self.user.username)
