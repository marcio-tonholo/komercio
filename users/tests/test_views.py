from rest_framework.test import APITestCase
from ..models import User

class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_seller = User.objects.create_user(
            email= "seller_test@mail.com",
            password="abcd",
            first_name= "test",
            last_name= "test",
            is_seller = True)

        cls.test_superuser = User.objects.create_superuser(
            email= "supeuser_test@mail.com",
            password="abcd",
            first_name= "test",
            last_name= "test",
            )

        cls.test_costumer = User.objects.create_user(
            email= "costumer_test@mail.com",
            password="abcd",
            first_name= "test",
            last_name= "test")

        cls.wrong_keys_response = {
            "email": ["This field is required."],
            "first_name": ["This field is required."],
            "last_name": ["This field is required."],
            "is_seller": ["This field is required."],
            "password": ["This field is required."]
        }

        cls.sellers= [User.objects.create(
            email= f'{user_id}@mail.com',
            password="abcd",
            first_name= "test",
            last_name= "test",
            is_seller= True)for user_id in range(1, 6)]

    def test_can_list_all_users(self):    
        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data),4) 

    def test_can_register_an_seller(self):    
        response = self.client.post('/api/accounts/',{
            "email": "test@mail.com",
            "password": "abcd",
            "first_name": "test",
            "last_name": "test",
            "is_seller": True
            }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(
            response.data
        )            

    def test_can_register_an_costumer(self):    
        response = self.client.post('/api/accounts/',{
            "email": "test@mail.com",
            "password": "abcd",
            "first_name": "test",
            "last_name": "test",
            "is_seller": False
            }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(
            response.data,
        )    

    def test_cannot_register_with_wrong_keys(self):    
        response = self.client.post('/api/accounts/',{}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEquals(
            response.data,self.wrong_keys_response
        )  

    def test_seller_can_login(self):  
        response = self.client.post('/api/login/',{"email":self.test_seller.email,
        "password":"abcd"},format = 'json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token",
            response.data
        )    

    def test_costumer_can_login(self):   
        response = self.client.post('/api/login/',{"email":self.test_costumer.email,
            "password": "abcd"}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("token",
            response.data
        )    
        
    def test_only_account_owner_can_update(self):
        self.client.force_authenticate(user=self.test_costumer)

        worng_response = self.client.patch(f'/api/accounts/{self.test_seller.id}/',{"email": "test2@mail.com"}, format='json') 
        self.assertEqual(worng_response.status_code, 403)  
        
        self.client.force_authenticate(user=self.test_seller)

        response = self.client.patch(f'/api/accounts/{self.test_seller.id}/',{"email": "test2@mail.com"}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_only_account_owner_or_superuser_can_update_is_active(self):
        self.client.force_authenticate(user=self.test_costumer)

        worng_response = self.client.patch(f'/api/accounts/{self.test_seller.id}/',{"is_active":False}, format='json') 
        self.assertEqual(worng_response.status_code, 403)  
        
        self.client.force_authenticate(user=self.test_seller)

        response = self.client.patch(f'/api/accounts/{self.test_seller.id}/',{"is_active":False}, format='json')
        self.assertEqual(response.status_code, 200)  

        self.client.force_authenticate(user=self.test_superuser)

        response = self.client.patch(f'/api/accounts/{self.test_seller.id}/',{"is_active":True}, format='json')
        self.assertEqual(response.status_code, 200)  

    
        
        