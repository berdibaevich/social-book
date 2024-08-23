
from django.shortcuts import render,redirect
from account.models import Account
from notification.models import Notification
from myaccount.models import MyAccount
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.db.models import Count

from book.models import (
    Tag,
    Book
)
from question.models import Question

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.paginator import Paginator, EmptyPage

from chat.models import DiscussBook

from django.db.models import Q




# Create your views here.

# 404 PAGE
def handler404(request, exception):
    return render(request, '404.html', status=404)
# END 404 PAGE

# 500 SERVER ERROR
def server_error(request):
    return render(request, '500.html', status=500)
# END 500 SERVER ERROR

#search function

def search_view(request):
    q = request.GET.get('q') if request.GET.get('q') != '' else None
    if q is not None:
        books = Book.objects.filter(
            Q(name__icontains = q)|
            Q(owner__username__icontains = q)|
            Q(tag__title__icontains = q)|
            Q(language__icontains = q)
        )

    else:
        return redirect('/')


    # active users
    active_users = [user for user in Account.objects.all() if user.owner_of_book.all().count() >=3]
    #books tags
    tags = Tag.objects.all()


    context = {
        'books': books,
        'active_users': active_users,
        'tags': tags
    }
    return render(request, 'search.html', context)




# ACTIVE USERS GET NUMBER
def get_active_user():
    """
    This function help us to know how many users has been published book
    active_users = [user for user in Account.objects.all() if user.owner_of_book.all().count() >=3]
    """

    active_users = Account.objects.annotate(count_nums = Count("owner_of_book")).filter(count_nums__gte = 3)
    return active_users
# END ACTIVE USERS GET NUMBER

# GET TAGS OF THE BOOK
def get_tags():
    return Tag.objects.annotate(nums_of_book = Count("tag_of_book")).all()
# END GET TAGS OF THE BOOK

# FILTER BOOKS OR NOT
def get_books(request):
    q = request.GET.get('q')
    if q == 'all' or q == None:
        obj = Book.objects.select_related("owner", "tag").prefetch_related("book_star", "views").all()
        return obj
    return Book.objects.select_related("owner", "tag").prefetch_related("book_star", "views").filter(tag__title = q)
# END FILTER BOOKS OR NOT



# HOME VIEWS
def home(request):
    user = request.user
    #Notifications 
    notification = Notification.objects.filter(receiver__username = user).first()
    counting_how_many = Notification.objects.filter(receiver__username = user, is_seen = False).count()



    # filter book
    books = get_books(request)
   

    # Paginations
    p = Paginator(books, 5)
    page_number = request.GET.get('page', 1)

    try:
        pages = p.page(page_number)
    except EmptyPage:
        pages = p.page(1)


    # Robot process
  
    count = 0 #how many message sent it
    robot = request.session.get('me')
    questions = None
    messages = {}
    if request.user.is_authenticated:
        book = Book.objects.select_related("owner").filter(owner = request.user).count()
        if book == 0:
            request.session['me'] = True
        
           
           
        request.session['me'] = False

        questions = Question.objects.select_related("user").filter(is_answered = False).exclude(user = request.user)
        count += len(questions)
        if len(questions) == 1:
            messages['question'] = 'we have question to which there are no answer'

        else:
            messages['question'] = 'we have questions to which there are no answers'



    

    
    
    elif robot is None:
        messages['welcome'] = 'Welcome to our My Social Book'
        messages['robot'] = 'Hi I am Robot'
        messages['help'] = 'I am glad to help you!'
        messages['ask'] = 'Do you have an account or not?'
        
        count = 2

      
        
    #get discuss if is_ready = True bols
    discuss_books = DiscussBook.objects.select_related("owner", "book", "user").prefetch_related("discussion_users").filter(is_ready = True, is_start = False).first()
    #get discuss room
    discusss = DiscussBook.objects.select_related("owner", "book", "user").prefetch_related("discussion_users").filter(is_start = True).first()

   


    context = {
        'noti': notification,
        'how_may': counting_how_many,
        'tags': get_tags(),
        'books': pages,
        'active_users': get_active_user(),
        'message': messages,
        'robot': robot,
        'count': count,
        'questions': questions,
        'discuss': discuss_books,
        'discusss': discusss
        
    }

    return render(request, 'home.html', context)






def accept_to_friends_list_view(request, *args, **kwargs):
    
    if request.method == 'GET':
        receiver = request.GET.get('receiver')
        sender = request.GET.get('sender')
        account = Account.objects.get(username = sender)
        
        my_account = MyAccount.objects.filter(account__username = receiver).first()
        my_account.friends.add(account)
        is_seen = Notification.objects.filter(receiver__username = receiver, sender__username = sender).first()
        if is_seen.how_many == 1:
            is_seen.is_seen = True
            is_seen.how_many -= 1
            is_seen.save()

        
    return HttpResponse('Succesgo')





def cancel_follower_to_accept(request):
    if request.method == 'GET':
        receiver = request.GET.get('receiver')
        sender = request.GET.get('sender')
        account_sender = Account.objects.get(username = sender)
        account_receiver = Account.objects.get(username = receiver)

        obj = Notification.objects.get(sender = account_sender, receiver = account_receiver)
        obj.delete()
        return redirect('notification:notification-view', account_receiver.pk)
    
    return HttpResponse('Successgooo!')










#download as pdf file

def download_as_pdf(request, book_name):
    book = Book.objects.get(name = book_name)
    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    obj = [
        book.name,
        book.subtitle
    ]
    for line in obj:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='book.pdf')
