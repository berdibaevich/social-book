
from django.test import TestCase, Client
from django.urls import resolve, reverse
from .views import home
# Create your tests here.


class HomePageTest(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    #test home func from view ok
    def test_list_url_is_resolved(self):
        url = reverse('home')
        
        self.assertEqual(resolve(url).func, home)
        