from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ChatOnetoOne, DiscussBook, ChatText
from account.models import Account
from django.http import JsonResponse
from book.models import Book
from notification.models import Notification
import datetime
from aboutbook.models import Discuss

# Create your views here.



#close chat room

def close_chat_view(request, room_name):
    user = request.user
    room = DiscussBook.objects.get(book__name = room_name)

    if request.method == 'POST':
        discussbook = DiscussBook.objects.all().filter(book__name = room).delete()
        chat_text = ChatText.objects.all().filter(room__name = room).delete()
        discuss = Discuss.objects.filter(book__name = room).delete()
        noti_time = Notification.objects.filter(receiver = user, book__name = room, notification_types = 5).delete()
        noti_agree = Notification.objects.filter(receiver = user, book__name = room, notification_types = 4).delete()
        
        messages.success(request, 'Chat room succesfully closed!')
        return redirect('/')

    context = {
        'room': room
    }
    return render(request, 'chat/close.html', context)




#room

def rooom(request, room):
    room = DiscussBook.objects.get(book__name = room)
    book = Book.objects.get(name = room.book.name)

    texts = ChatText.objects.all().filter(room = book).order_by('-created')

    rooms = DiscussBook.objects.all().filter(book__name = room)

    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            room = rooms[0]
            text = request.POST.get('text')
            
            if user in room.discussion_users.all():
                if text != '':
                    ChatText.objects.create(
                        room = book,
                        user = user,
                        text = text
                    )

                else:
                    messages.warning(request, 'Sorry you can\'t write empty message')
                    return redirect('chat:room', room)
            else:   
                room.discussion_users.add(user)




    context = {
        'room': room,
        'texts': texts
    }

    return render(request, 'chat/rooms.html', context)



#Get object which discusstion room's timer out
def start_is_true_view(request):
    if request.method == 'GET':
        book_name = request.GET.get('book_name')
        discuss = DiscussBook.objects.get(book__name = book_name)
        discuss.is_start = True
        discuss.save()
        


        return JsonResponse({'data': 'Saved!!'})







#get when will start disscuss time

def start_discuss(request):
    
    user = request.user
    if request.method == 'GET':
        book = request.GET.get('book_name')
        time = request.GET.get('time')
        date = request.GET.get('date')
        discussbook = DiscussBook.objects.filter(owner=user, book__name = book).first()

        y, m, day = date.split('-')
        h, minut = time.split(':')
         
        day_get = day if day[0] != '0' else day[-1]
        months = m if m[0] !='0' else m[-1]
        get_date = datetime.datetime(year=int(y), month=int(months), day=int(day_get), hour=int(h), minute=int(minut))

        discuss_models = Discuss.objects.filter(book__name = book).first()
        
        # When user add time when to start discuss so we gonna is_seen also add is True in Notifications

        noti_is_seen = Notification.objects.filter(sender = user, receiver = user, book__name = book, notification_types = 5).first()
        
        for user in discuss_models.users.all():
            discussbook.discussion_users.add(user)

        discussbook.when = get_date
        discussbook.is_ready = True
        discussbook.save()


        noti_is_seen.is_seen = True
        noti_is_seen.save()
        
        return JsonResponse({'data': 'saved'})




#Create for discussion room

def create_room(request):
    user = request.user

    if request.method == 'GET':
        book_pk = request.GET.get('book_pk')
        count = request.GET.get('count')
        book = Book.objects.get(pk = book_pk)
        

        discussbook = DiscussBook.objects.filter(owner = user, book = book)
        if not discussbook.exists():
            dis_book = DiscussBook.objects.create(
                owner = user,
                book = book
            )
            #Notifications process
            noti, created = Notification.objects.get_or_create(sender = user, receiver = user, book = book, notification_types = 5)
            noti.message_text = 'You created room so you need to add time when you gonna start to discuss!!'
            noti.save()

            


        return JsonResponse({'data': 'Succesfully created!'})








@csrf_exempt
def get_message_from_js(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('name')
        text = request.POST.get('text')
        receiver = Account.objects.get(username = username)
        ChatOnetoOne.objects.create(
            user = request.user,
            sender = request.user,
            receiver = receiver,
            body = text
        )
        
        return JsonResponse({'data': 'Data saved'})

    else:
        return JsonResponse({'data': 'data Not saved'})





def send_message_view(request):
    user = request.user

    if request.method == 'POST':
        receiver_pk = request.POST.get('receiver')
        text = request.POST.get('text') or None
        account = Account.objects.get(pk = receiver_pk)
     
        if text is not None:
            ChatOnetoOne.objects.create(
                user = user,
                sender = user,
                receiver = account,
                body = text
            )

     

        else:
            messages.error(request, "You can't send an empty message!!")
            return redirect('myaccount:my-account', receiver_pk)



        return redirect('myaccount:my-account', receiver_pk)
