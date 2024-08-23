from django.test import TestCase, Client
from .models import Tag, Book
from account.models import Account
from django.urls import reverse, resolve
from .views import book_detail_view, add_book
import tempfile
from .forms import BookForm

# Create your tests here.



class BookAndTagTest(TestCase):
    def setUp(self) -> None:
        
        self.user1 = Account.objects.create_user(
            email = 'user@a.com',
            username = 'user',
            password = '12234'
        )

        self.tag1 = Tag.objects.create(
            title = 'programming'
        )
       

        self.book1 = Book.objects.create(
            owner = self.user1,
            tag = self.tag1,
            language = 'uz',
            name = 'Python for everybody',
            subtitle = 'Yeaa',
            author = 'yeaa',
            feedback = 'nooo',
            image = tempfile.NamedTemporaryFile(suffix=".jpg").name #like this we don't need a real file to our test


        )



    #form model we test __str__
    def test_tag_book_str(self):
        tag = str(self.tag1)
        book = str(self.book1)
        book_content = 'user.Book is Python for everybody and Tag is programming'
        tag_content = 'programming'
        self.assertEqual(tag, tag_content)
        self.assertEqual(book, book_content)





    #tag model has property count book we test it
    def test_count_book_from_tag(self):
        tag_count = self.tag1.count_book
        self.assertEqual(tag_count, 1)





    #testing detail view url
    def test_book_detail(self):
        book = Book.objects.get(pk = 1)
        url = reverse('book:detail', kwargs={'pk': book.pk})
        self.assertEqual(url, '/book/1/')


    


    #testing detail function view
    def test_book_detail_view(self):
        url = reverse('book:detail', args=[self.book1.pk])
        self.assertEqual(resolve(url).func, book_detail_view)




    #response test for detail book and also template html test
    def test_book_detail_GET(self):
        client = Client()
        response = client.get(reverse('book:detail', kwargs={'pk': self.book1.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'book/book_detail.html')




    #test add book function view from views.py
    def test_add_book_view(self):
        url = reverse('book:add-book')
        self.assertEqual(resolve(url).func, add_book)


    
    #testing add book view and template ok
    def test_add_book_view(self):
        login = self.client.login(
            email = 'user@a.com',
            password = '12234'
        )

        self.assertTrue(login) #after login it gives us True if user login

        response = self.client.get(reverse('home')) #after login page moved to home

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        

        url = self.client.get(reverse('book:add-book'))

        #testing add book
        add_response = self.client.post(
            reverse('book:add-book'),
            {
                'owner':self.user1,
                'tag': self.tag1,
                'language': 'eng',
                'name': 'Django for everyone',
                'subtitle': 'yeaaa',
                'author': 'django Kim',
                'image': tempfile.NamedTemporaryFile(suffix=".jpg").name,
                'feedback': 'this book is great'

            }
        )

        self.assertEquals(add_response.status_code, 200)
        
        self.assertTemplateUsed(url, 'book/add_book.html')






# class BookFormTest(TestCase):
#     def setUp(self) -> None:
#         self.user = Account.objects.create_user(
#             username = 'user',
#             email = 'a@a.com',
#             password = 'user'
#         )

#         self.tag = Tag.objects.create(title = 'django')
    
#     def test_form_valid_data(self):
        
#         image = tempfile.NamedTemporaryFile(suffix=".jpg").name
#         form = BookForm(data={
#             'language': 'uz',
#             'name': 'DJango',
#             'subtitle': 'This',
#             'author': 'Jonh',
#             'feedback': 'Good',
            
#         })
#         # form.instance.owner = self.user
#         # form.instance.tag = self.tag

#         # self.assertTrue(form.is_valid())

#         print(form.errors)
        
        




