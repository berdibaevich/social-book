from django.shortcuts import render, redirect
from django.contrib import messages
from book.models import Book
from account.models import Account
from .models import Like, Dislike
from notification.models import Notification



# Create your views here.


#like views
def like_view(request, *args, **kwargs):
    current_user = request.user

    book = kwargs.get('book')
    username = kwargs.get('username')
    get_book = Book.objects.filter(name = book).first()
    user = Account.objects.filter(username = username).first()



    if username == 'AnonymousUser':
        messages.warning(request, 'Siz dizimnen yamasa loginnen otpegensiz')
        return redirect('book:detail', get_book.pk)

    

    liked_book = Like.objects.get(book = get_book)
    disliked_book = Dislike.objects.get(book = get_book)
    

    if user not in liked_book.users.all() and user not in disliked_book.users.all():
        liked_book.counter += 1
        liked_book.save()
        liked_book.users.add(user)
        

        #notification process comes up
        if current_user != get_book.owner:
            get_notification, created = Notification.objects.get_or_create(sender = current_user, receiver = get_book.owner, book = get_book)

            get_notification.notification_types = 1
            get_notification.message_text = f'Sizge "{current_user.username}" paydalaniwshidan bir dana Like'
            get_notification.how_many += 1
            get_notification.save()



    elif user in liked_book.users.all() and user not in disliked_book.users.all():
        liked_book.counter -= 1
        liked_book.save()
        liked_book.users.remove(user)



    elif user not in liked_book.users.all() and user in disliked_book.users.all():
        liked_book.counter += 1
        liked_book.save()
        liked_book.users.add(user)


        disliked_book.counter -= 1
        disliked_book.save()
        disliked_book.users.remove(user)

        #notification process comes up
        if current_user != get_book.owner:
            get_notification, created = Notification.objects.get_or_create(sender = current_user, receiver = get_book.owner, book = get_book)

            get_notification.notification_types = 1
            get_notification.message_text = f'Sizge "{current_user.username}" paydalaniwshidan bir dana Like'
            get_notification.how_many += 1
            get_notification.save()
        


    return redirect('book:detail', get_book.pk)









# Dislike View

def dislike_view(request, *args, **kwargs):
    book = kwargs.get('book')
    username = kwargs.get('username')
    get_book = Book.objects.filter(name = book).first()
    user = Account.objects.filter(username = username).first()

    if username == 'AnonymousUser':
        messages.warning(request, 'Siz dizimnen yamasa loginnen otpegensiz')
        return redirect('book:detail', get_book.pk)


    liked_book = Like.objects.get(book = get_book)
    disliked_book = Dislike.objects.get(book = get_book)

    if user not in disliked_book.users.all() and user not in liked_book.users.all():
        disliked_book.counter += 1
        disliked_book.save()
        disliked_book.users.add(user)



    elif user in disliked_book.users.all() and user not in liked_book.users.all():
        disliked_book.counter -= 1
        disliked_book.save()
        disliked_book.users.remove(user)



    elif user not in disliked_book.users.all() and user in liked_book.users.all():
        disliked_book.counter += 1
        disliked_book.save()
        disliked_book.users.add(user)

        liked_book.counter -= 1
        liked_book.save()
        liked_book.users.remove(user)
    



    return redirect('book:detail', get_book.pk)
    
    
    