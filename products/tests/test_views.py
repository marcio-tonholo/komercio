from rest_framework.test import APITestCase
from users.models import User


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.wrong_keys_response = {
            "description": ["This field is required."],
            "price": ["This field is required."],
            "quantity": ["This field is required."]
            }

        cls.test_seller1 = User.objects.create_user(
        email= "seller_test@mail.com",
        password="abcd",
        first_name= "test",
        last_name= "test",
        is_seller = True)

        cls.test_seller2 = User.objects.create_user(
        email= "seller2_test@mail.com",
        password="abcd",
        first_name= "test",
        last_name= "test",
        is_seller = True)

        cls.test_costumer = User.objects.create_user(
            email= "costumer_test@mail.com",
            password="abcd",
            first_name= "test",
            last_name= "test")


    def test_can_list_all_users(self):    
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data),4)  
        
    def test_not_equal_responses(self):
        self.client.force_authenticate(user=self.test_seller1)
        post_response = self.client.post('/api/products/',{
            "description":"Peixe astronauta",
            "price":190.20,
            "quantity":10
        }, format='json')    

        get_response = self.client.get('/api/products/')       

        self.assertNotEqual(post_response,get_response)

    def test_only_seller_can_register_an_product(self):
        self.client.force_authenticate(user=self.test_costumer)
        response = self.client.post('/api/products/',{
            "description":"Peixe astronauta",
            "price":190.20,
            "quantity":10
        }, format='json')

        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.test_seller1)
        response = self.client.post('/api/products/',{
            "description":"Peixe astronauta",
            "price":190.20,
            "quantity":10
        }, format='json')
        
        
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data)

    def test_only_product_seller_can_update(self):
        self.client.force_authenticate(user=self.test_seller1)
        product = self.client.post('/api/products/',{
            "description":"Peixe astronauta",
            "price":190.20,
            "quantity":10
        }, format='json')

        self.client.force_authenticate(user=self.test_seller2)
        response = self.client.patch(f'/api/products/{product.data["id"]}/',{"description":"Test"}, format='json')
        
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.test_seller1)
        response = self.client.patch(f'/api/products/{product.data["id"]}/',{"description":"Test"}, format='json')
        
        self.assertEqual(response.status_code, 200)


    def test_cannot_register_product_with_wrong_keys(self):

        self.client.force_authenticate(user=self.test_seller1)    
        response = self.client.post('/api/products/',{}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEquals(
            response.data,self.wrong_keys_response
        )    

    def test_cannot_create_product_whith_negative_quatity(self):  
        self.client.force_authenticate(user=self.test_seller1)
        response = self.client.post('/api/products/',{
            "description":"Peixe astronauta",
            "price":190.20,
            "quantity":-10
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
	        "quantity": ["Ensure this value is greater than or equal to 0."]
            })  