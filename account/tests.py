
from django.test import TestCase
from django.conf import settings
from .models import Account
from .forms import RegisterForm


# Create your tests here.



class AccountTestCase(TestCase):

    def setUp(self) -> None:
        user_a = Account(username = 'jetker', email = 'jetker@gmail.com')
        user_a.set_password('admin')
        user_a.is_staff = True
        user_a.is_admin = True
        user_a.is_superuser = True
        user_a.save()
        self.user_a = user_a

        # second user which is not staff and superuser
        user_b = Account.objects.create_user(
            username = 'test1',
            email = 'test@gmail.com',
            password = 'test'
        )
        self.user_b = user_b

    

    # Account test which is created up is gives us True
    def test_user_exists(self):
        user_qs = Account.objects.all()
        self.assertTrue(user_qs.exists())
        self.assertEqual(user_qs.count(), 2)
    
    # Second test 
    def test_user_is_staff_or_not(self):
        user_is_staff = Account.objects.get(username = self.user_a)
        user_not_is_staff = Account.objects.get(username = self.user_b)
        # check this user_is_staff
        self.assertTrue(user_is_staff.is_staff)
        # check second user
        self.assertEqual(user_not_is_staff.is_staff, False)




        