
from django.test import TestCase
from .models import WillRead, Discuss, Readed, Reading
from account.models import Account
from book.models import Book, Tag
from django.urls import reverse, resolve

import tempfile




# Create your tests here.

class AboutBookModelTest(TestCase):
    
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            username = 'user1',
            email = 'a@a.com',
            password = 'admin'
        )


        self.tag = Tag.objects.create(
            title = 'programming'
        )
      

        self.book = Book.objects.create(
            owner = self.user,
            tag = self.tag,
            language = 'uz',
            name = 'Python for everybody',
            subtitle = 'Yeaa',
            author = 'yeaa',
            feedback = 'nooo',
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name #like this we don't need a real file to our test

        )

        self.reading = Reading(
            book = self.book
        )


    
    def test_will_read_model(self):
        will_read = WillRead.objects.create(
            book = self.book
        )
        willRead = WillRead.objects.get(id = 1)

        self.assertEqual(str(willRead), 'Python for everybody')
        self.assertEqual(willRead.count, 0)

        self.assertNotEqual(willRead.count, 2)


    

    def test_will_read_user_agreed(self):
        will_read = WillRead.objects.create(
            book = self.book
        )

        user_john = Account.objects.create_user(
            username = 'john',
            email = 'john@a.com',
            password = '123441'
        )
        
        #login process
        login = self.client.login(
            email = 'john@a.com',
            password = '123441'
        )
        self.assertTrue(login)
        #after login go to home
        home = self.client.get(reverse('home'))
        #check user login or not
        self.assertEqual(str(home.context['user']), 'john')

        #we gonna go book detailView
        detail = self.client.get(reverse('book:detail', kwargs={'pk': self.book.pk}))

        self.assertEqual(detail.status_code, 200)

        #detailden userdi korip atirmiz 
        get_detail_user = detail.context['user']
        add_will_read = self.client.get(reverse('aboutbook:will_read', kwargs={'user': user_john.username, 'book_name': self.book.name}))

     

        if get_detail_user not in will_read.users.all():
            will_read.users.add(get_detail_user)


        self.assertEqual(self.book.get_willread(), 1)


    
    def test_reading_model(self):
        reading = str(self.reading)
        self.assertEqual(reading, 'Python for everybody')

        self.assertEqual(self.reading.count, 0)


    
    
        

        
        
        

        
        
        
        