from django.shortcuts import render, redirect

from .models import Notification
from account.models import Account
from myaccount.models import MyAccount
from chat.models import DiscussBook


from django.contrib import messages


# Create your views here.




def notification_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        
        pk = kwargs.get('pk')
        account = Account.objects.get(pk = pk)
        notification_receiver = Notification.objects.filter(receiver = account, is_seen = False).order_by('-created')




        #Bul jerde notification bir korgennen keyin is_seen = True
        #qilamiz onda bizler sessionnan paydalanamiz
        is_seen = request.session.get('is_seen') 

        if is_seen is None:
            request.session['is_seen'] = False

        if is_seen != True:
            for noti in notification_receiver:
                if noti.is_seen == False and noti.notification_types == 1:
                    noti.is_seen = True
                    noti.save()


                if noti.is_seen == False and noti.notification_types == 4:
                    noti.is_seen = True
                    noti.save()


        #this is be aware when someone's discussion room timer out 
        discuss = DiscussBook.objects.filter(is_ready = True, is_start = False)

        count = 0
        
        if discuss.count() == 0:
            count = 0

        else:
            count = 1

     
    

        
        



    else:
        messages.warning(request, 'You must be login!')
        return redirect('/')

    


    
    
    context = {
        'notifications': notification_receiver,
        'count': count,
        
    }
    



    return render(request, 'notification/notification_view.html', context)