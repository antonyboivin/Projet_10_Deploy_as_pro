from django.contrib import auth
from django.urls import reverse
from django.test import TestCase


# At first, I check that all pages of the application are functional.
class StatusCodePages(TestCase):
    """
        Class StatusCodePages ensures that all templates return a status code 200.
    """
    def setup(self):
        """
            The setup method contains :
                self.usertest creates a user for the test requirements.
        """
        self.usertest = User.objects.create_user('usertest', 'usertest@test.com', 'usertest')
        self.apiQuery = [{'nom':'nom du produit'}]
        self.userQuery = 'un produit'

    def test_home_page(self):
        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, 200)
    
    def test_sign_up_page(self):
        response = self.client.get(reverse('sign up'))
        self.assertEqual(response.status_code, 200)

    def test_connection_page(self):
        response = self.client.get(reverse('connection'))
        self.assertEqual(response.status_code, 200)
    
    def test_deconnection_page(self):
        response = self.client.get(reverse('deconnection'), follow=True)
        self.assertEqual(response.status_code, 200)
 
    def test_my_account_page(self):
        logged = self.client.login(username='usertest', password='usertest')
        if logged:
            response = self.client.get(reverse('my account'))
            self.assertEqual(response.status_code, 200)
            self.client.logout()

    def test_product_select_page(self):

        userQuery = 'nutella'
        apiQuery = [{'product_name_fr': 'Nutella', 'code': '3017620429484',
                     'nutrition_grade_fr': 'e', 'categories_hierarchy': ['fr:pates-a-tartiner'],
                     'categories': 'Desayunos,Untables,Untables dulces,Cremas para untar,Cremas de chocolate,Cremas a base de avellanas,Cremas de cacao y avellanas,Pâtes à tartiner',
                     'image_small_url': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.200.jpg'}]
        response = self.client.post('/substitution_app/product_select/', {'apiQuery': apiQuery, 'userQuery' : userQuery})
        self.assertEqual(response.status_code, 200)


# 
class CallTheApi(TestCase):
    pass