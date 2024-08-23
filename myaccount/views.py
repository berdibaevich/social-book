from django.shortcuts import render, redirect
from .models import MyAccount, Follow
from account.models import Account
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import MyImageForm, MyAccountForm
from notification.models import Notification
from book.models import Book

from django.http import FileResponse
import io
from chat.models import ChatOnetoOne
import json
# Create your views here.




# My Account page view
@login_required
def my_account_view(request, *args, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    try:
        account = Account.objects.get(pk = pk)
        
    except Account.DoesNotExist:
        messages.error(request, 'Bunday account iyesi tabilmadi!!')
        return redirect('/')

    my_account = MyAccount.objects.get(account = account)

    # Get message from chat
    
        
    chats = ChatOnetoOne.objects.filter(receiver = user, is_read = False).order_by('-time')

  
    
        
    
    

    
    #how many books has
    count = Book.objects.filter(owner = account).count()
    

    # change image
    form = MyImageForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        obj = form.cleaned_data.get('profile_img')
        print(obj)
        form.save()
        return JsonResponse({'message': 'Works'})
    # / change image

    # Define follower or not
    is_follower = False
    follow, created = Follow.objects.get_or_create(user = account)
    count_following = follow.following.all().count()
    
    if user in follow.follower.all():
        is_follower = True
    
    else:
        is_follower = False
    # //

    # get boooks and saved data
    books = True
    
    saved_books = request.GET.get('q')
    if saved_books is not None:
        books = False
    else:
        books = True


    boooks = Book.objects.filter(owner = account)


    #when current user checked message as read so we gonna change is_read True
    if request.method == 'GET':
        username = request.GET.get('username')
        chat = ChatOnetoOne.objects.filter(sender__username = username,receiver = user)

        if chat.exists():
            for get_chat in chat:
                get_chat.is_read = True
                get_chat.save()

          


    context = {
        'my_account':my_account,
        'form': form,
        'is_follower': is_follower,
        'count_following': count_following,
        'count': count,
        'boooks': boooks,
        'books': books,
        'chats': chats

    }
    return render(request, 'myaccount/my_account.html', context)


# ////////


@login_required
def edit_my_account_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    my_account = MyAccount.objects.get(pk = pk)

    form =  MyAccountForm(request.POST or None, instance=my_account)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.account = request.user
        obj.save()
        messages.success(request, f"Your profile successfuly updated!")
        return redirect('myaccount:my-account', request.user.pk)



    context = {
        'form': form
    }

    return render(request, 'myaccount/edit-myaccount.html', context)






#Follower and following protsess

def follow_view(request, *args, **kwargs):

    user = request.user
    pk = kwargs.get('pk')
    account = Account.objects.get(pk = pk)
    my_followers = MyAccount.objects.get(account = account)
    get_user, created = Follow.objects.get_or_create(user = account)
    
    
    if user != account:
        
        following_user, created = Follow.objects.get_or_create(user = user)
        if user not in get_user.follower.all() and account not in following_user.following.all():
            get_user.follower.add(user)
            following_user.following.add(account)
            my_followers.followers += 1
            my_followers.save()

            # notifications process
            notification, created = Notification.objects.get_or_create(receiver = account, sender = user)
            notification.notification_types = 3
            notification.message_text = f"{user} followed to your profile.If you wanna accept this {user} to your friends list.Please accept or cancel"
            notification.how_many = 1
            notification.save()
       
        else:
            get_user.follower.remove(user)
            following_user.following.remove(account)
            my_followers.followers -= 1
            my_followers.save()


        


    else:
        messages.info(request, 'Sorry Siz ozin\'izge following qila almaysiz!!')
        return redirect('myaccount:my-account', pk)




    return redirect('myaccount:my-account', pk)







#Saved book from another user

def save_book(request, *args, **kwargs):
    user = kwargs.get('user')
    book = kwargs.get('book')
    if user == 'AnonymousUser':
        messages.warning(request, 'Dizimnen yamasa loginnen o\'tpegensiz!')
        return redirect('/')

    book = Book.objects.filter(name = book).first()
    my_account = MyAccount.objects.get(account__username = user)
    
    
    if my_account.account != book.owner:
        if book not in my_account.favorites_book.all():
            my_account.favorites_book.add(book)

            messages.success(request, 'Mag\'liwmat awmetli saqlang\'an!')
            return redirect('/')
        else:
            messages.warning(request, 'Sizde bul kitap haqida mag\'liwmat saqlang\'an!')
            return redirect('/')
    
    else:
        messages.warning(request, 'Siz o\'z kitabiniz haqida mag\'liwmatdi saqlay almaysiz!')
        return redirect('/')
    




