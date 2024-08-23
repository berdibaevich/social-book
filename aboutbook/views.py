from django.shortcuts import render, redirect
from django.contrib import messages
from book.models import Book
from account.models import Account
from notification.models import Notification
from chat.models import DiscussBook

from .models import (
    Readed,
    Reading,
    WillRead,
    Discuss
)

# Create your views here.



#reading boook
def reading_book_view(request, *args, **kwargs):
    book_name = kwargs.get('book_name')
    user_username = kwargs.get('user')
    book = Book.objects.filter(name = book_name).first()
    
    
    if user_username == 'AnonymousUser':
        messages.error(request, 'Mag\'liwmat saqlanbadi. Siz dizimnen yamasa loginnen otiwin\'iz kerek!')
        return redirect('book:detail', book.pk)

    get_reading, created = Reading.objects.get_or_create(book = book)
    get_readed, created = Readed.objects.get_or_create(book = book)
    get_willread, created = WillRead.objects.get_or_create(book = book)
    get_discuss, created = Discuss.objects.get_or_create(book = book)
    

    user = Account.objects.get(username = user_username)


    if user != book.owner:
        if user not in get_willread.users.all():

            if user not in get_readed.users.all():
                if user not in get_reading.users.all():
                    get_reading.users.add(user)
                    get_reading.count += 1
                    get_reading.save()
                    messages.success(request, 'Mag\'liwmat awmetli saqlandi!')
                    return redirect('book:detail', book.pk)
                
                else:
                    messages.warning(request, 'Siz oqip atirgan ediniz!')
                    return redirect('book:detail', book.pk)

            else:
                messages.warning(request, 'Siz oqip boldim dep edin\'iz!')
                return redirect('book:detail', book.pk)

        else:
            get_willread.users.remove(user)
            get_willread.count -= 1
            get_willread.save()


            get_reading.users.add(user)
            get_reading.count += 1
            get_reading.save()
            messages.success(request, 'Mag\'liwmat awmetli saqlandi!')
            return redirect('book:detail', book.pk)



    else:
        messages.warning(request, 'Siz o\'z oqig\'an kitabin\'izg\'a kirite almaysiz!')
        return redirect('book:detail', book.pk)













#already get readed

def readed_book_view(request, *args, **kwargs):
    book_name = kwargs.get('book_name')
    user_username = kwargs.get('user')
    book = Book.objects.filter(name = book_name).first()

    if user_username == 'AnonymousUser':
        messages.error(request, 'Mag\'liwmat saqlanbadi. Siz dizimnen yamasa loginnen otiwin\'iz kerek!')
        return redirect('book:detail', book.pk)


    user = Account.objects.get(username = user_username)

    get_reading, created = Reading.objects.get_or_create(book = book)
    get_readed, created = Readed.objects.get_or_create(book = book)
    get_willread, created = WillRead.objects.get_or_create(book = book)
    get_discuss, created = Discuss.objects.get_or_create(book = book)
    

    if user != book.owner:
        if user not in get_discuss.users.all():
            if user not in get_readed.users.all():
                get_readed.users.add(user)
                get_readed.count += 1
                get_readed.save()
                messages.success(request, 'Mag\'liwmat saqlandi')
                return redirect('book:detail', book.pk)
            
            else:
                messages.success(request, 'Sizde oqip boldim degen mag\'liwmat aldin saqlang\'an!')
                return redirect('book:detail', book.pk)

        else:
            messages.success(request, 'Siz dodalaw yag\'niy oz ara pikir almasiw dizimine qosilg\'ansiz')
            return redirect('book:detail', book.pk)

    else:
        messages.warning(request, 'Siz o\'z oqig\'an kitabin\'izg\'a kirite almaysiz!')
        return redirect('book:detail', book.pk)







#will read

def will_read_book_view(request, *args, **kwargs):
    book_name = kwargs.get('book_name')
    user_username = kwargs.get('user')
    book = Book.objects.filter(name = book_name).first()

    if user_username == 'AnonymousUser':
        messages.error(request, 'Mag\'liwmat saqlanbadi. Siz dizimnen yamasa loginnen otiwin\'iz kerek!')
        return redirect('book:detail', book.pk)

    user = Account.objects.get(username = user_username)

    get_reading, created = Reading.objects.get_or_create(book = book)
    get_readed, created = Readed.objects.get_or_create(book = book)
    get_willread, created = WillRead.objects.get_or_create(book = book)
    get_discuss, created = Discuss.objects.get_or_create(book = book)
    

    if user != book.owner:
        if user not in get_reading.users.all():
            if user not in get_readed.users.all():
                if user not in get_discuss.users.all():
                    if user not in get_willread.users.all():
                        get_willread.users.add(user)
                        get_willread.count += 1
                        get_willread.save()
                        messages.success(request, 'Mag\'liwmat saqlandi')
                        return redirect('book:detail', book.pk)

                    else:
                        messages.warning(request, 'Siz aldin kiritkensiz!')
                        return redirect('book:detail', book.pk)

                else:
                    messages.success(request, 'Siz dodalaw yag\'niy oz ara pikir almasiw dizimine qosilg\'ansiz')
                    return redirect('book:detail', book.pk)

            else:
                messages.warning(request, 'Siz ol kitapdi oqip bolg\'ansiz!')
                return redirect('book:detail', book.pk)


        else:
            messages.warning(request, 'Siz oqip atirman dep ediniz!')
            return redirect('book:detail', book.pk)


    else:
        messages.warning(request, 'Siz o\'z oqig\'an kitabin\'izg\'a kirite almaysiz!')
        return redirect('book:detail', book.pk)







#discuss about thiss book
def discuss_view(request, *args, **kwargs):
    book_name = kwargs.get('book_name')
    user_username = kwargs.get('user')
    book = Book.objects.filter(name = book_name).first()

    if user_username == 'AnonymousUser':
        messages.error(request, 'Mag\'liwmat saqlanbadi. Siz dizimnen yamasa loginnen otiwin\'iz kerek!')
        return redirect('book:detail', book.pk)

    user = Account.objects.get(username = user_username)

    get_reading, created = Reading.objects.get_or_create(book = book)
    get_readed, created = Readed.objects.get_or_create(book = book)
    get_willread, created = WillRead.objects.get_or_create(book = book)
    get_discuss, created = Discuss.objects.get_or_create(book = book)
    

    


    if user != book.owner:
        if user not in get_willread.users.all():
            if user not in get_discuss.users.all():
                get_discuss.users.add(user)
                get_discuss.count += 1
                get_discuss.save()

                if get_discuss.count == 5:
                    noti, created = Notification.objects.get_or_create(sender = book.owner, receiver = book.owner, book = book, notification_types = 5)
                    noti.message_text = 'Your room automatically created so you need to add time when you gonna start to discuss!!'
                    noti.save()

                    discussbook = DiscussBook.objects.filter(owner = book.owner, book = book).exists()
                    
                    if not discussbook:
                        obj = DiscussBook.objects.create(
                            owner = book.owner,
                            book = book
                        )
                        for user in get_discuss.users.all():
                            obj.discussion_users.add(user)

                    


                else:
                    notification, created = Notification.objects.get_or_create(sender = user, receiver = book.owner, notification_types = 4, book = book)
                    notification.message_text = f'Paydalaniwshi {user} pikir almasiwin ushin qosildi. Endi Chatg\'a {5 - get_discuss.count} - adam qaldi!!'
                    notification.save()


                

               
                    



                messages.success(request, f'Mag\'liwmat saqlandi. {5 - get_discuss.count} - userden keyin dodalaw yag\'niy oz-ara pikir almasiw chat boladi.Baslaniwdan aldin sizge eskertiw beriledi!!')
                return redirect('book:detail', book.pk)
                
                

                


            else:
                messages.success(request, 'Siz aldin kiritkensiz!')
                return redirect('book:detail', book.pk)
        else:
            messages.error(request, 'Siz usi kitap boyisha oqimadiniz!')
            return redirect('book:detail', book.pk)

    else:
        messages.warning(request, 'Siz o\'z oqig\'an kitabin\'izg\'a kirite almaysiz!')
        return redirect('book:detail', book.pk)



