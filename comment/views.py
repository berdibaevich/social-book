from django.shortcuts import render, redirect
from book.models import Book
from account.models import Account
from .models import ParentComment
from likeordislike.models import (
    Like, 
    Dislike
)
from django.contrib import messages
from .forms import ParentCommentForm




# Create your views here.



# Reply to parent comment view

def reply_to_comment_view(request, *args, **kwargs):
    book_pk = kwargs.get('book_pk')
    comment_pk = kwargs.get('comment_pk')
    book = Book.objects.get(pk = book_pk)
    comment = ParentComment.objects.get(pk = comment_pk)
    form = ParentCommentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.book = book
        obj.parent = comment
        obj.save()
        return redirect('book:detail', book.pk)











# Like to comment view function
def like_comment_view(request, *args, **kwargs):
    username = kwargs.get('username')

    book_name = kwargs.get('book')
    comment_text = kwargs.get('text')
    comment_user = kwargs.get('comment_user')


    book = Book.objects.get(name = book_name)

    comment = ParentComment.objects.filter(book=book, user__username = comment_user, text = comment_text).first()
    


    if username != 'AnonymousUser':
        like_comment, created = Like.objects.get_or_create(comment = comment)
        dislike_comment, created = Dislike.objects.get_or_create(comment = comment)
        user = Account.objects.get(username = username)
        
        if user not in like_comment.users.all() and user not in dislike_comment.users.all():
            like_comment.users.add(user)
            like_comment.counter += 1
            like_comment.save()

            comment.likes.add(user)


        elif user in like_comment.users.all() and user not in dislike_comment.users.all():
            like_comment.users.remove(user)
            like_comment.counter -= 1
            like_comment.save()

            comment.likes.remove(user)

            


        elif user not in like_comment.users.all() and user in dislike_comment.users.all():
            like_comment.users.add(user)
            like_comment.counter += 1
            like_comment.save()

            comment.likes.add(user)

            dislike_comment.users.remove(user)
            dislike_comment.counter -= 1
            dislike_comment.save()

            comment.dislikes.remove(user)

        
        
 



    else:
        messages.warning(request, 'Siz dizimnen yamasa loginnen otpedin\'iz!')
        return redirect('book:detail', book.pk)

    



    return redirect('book:detail', book.pk)





#dislike btn comment view

def dislike_comment_view(request, *args, **kwargs):
    username = kwargs.get('username')
    book_name = kwargs.get('book')
    comment_text = kwargs.get('text')
    comment_user = kwargs.get('user')

    book = Book.objects.get(name = book_name)


    comment = ParentComment.objects.get(book = book, user__username = comment_user, text = comment_text)

    if username != 'AnonymousUser':
        like_comment, created = Like.objects.get_or_create(comment = comment)
        dislike_comment, created = Dislike.objects.get_or_create(comment = comment)
        user = Account.objects.get(username = username)

        if user not in dislike_comment.users.all() and user not in like_comment.users.all():
            dislike_comment.users.add(user)
            dislike_comment.counter += 1
            dislike_comment.save()

            comment.dislikes.add(user)

        elif user in dislike_comment.users.all() and user not in like_comment.users.all():
            dislike_comment.users.remove(user)
            dislike_comment.counter -= 1
            dislike_comment.save()

            comment.dislikes.remove(user)


        elif user not in dislike_comment.users.all() and user in like_comment.users.all():
            dislike_comment.users.add(user)
            dislike_comment.counter += 1
            dislike_comment.save()

            comment.dislikes.add(user)

            like_comment.users.remove(user)
            like_comment.counter -= 1
            like_comment.save()

            comment.likes.remove(user)





    else:
        messages.warning(request, 'Siz dizimnen yamasa loginnen otpedin\'iz!')
        return redirect('book:detail', book.pk)

    

    return redirect('book:detail', book.pk)

