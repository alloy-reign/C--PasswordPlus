from django.http import response
from django.test import TestCase
from .models import SavedPassword,User
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='testuser@gmail.com',password='testpassword',fname='test',lname='user')
    
    def checkUser(self):
        user = User.objects.get(email='testuser@gmail.com')
        self.assertEqual(user.fname,'test')

class SavedPassword(TestCase):
    def setUp(self):
        SavedPassword(user=User.objects.get(email='testuser@gmail.com'),password='testpassword',name='www.google.com',username='testuser')

    def checkSavedPassword(self):
        password = SavedPassword.objects.get(name='www.google.com')
        self.assertEqual(password.name,'www.google.com')


class ViewsTestCase(TestCase):

    def test_register_loads_properly(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)