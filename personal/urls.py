from django.urls import path
from django.conf.urls import handler404, handler500
from .views  import (
    home,
    accept_to_friends_list_view,
    cancel_follower_to_accept,
    download_as_pdf,
    search_view,

)



urlpatterns = [
    path('', home, name = 'home'),
    path('search/', search_view, name = 'search'),
    path('accept/', accept_to_friends_list_view, name = 'accept'),
    path('cancel/', cancel_follower_to_accept, name = 'cancel'),

    path('download/<book_name>/', download_as_pdf, name = 'download_as_pdf'),
    

    
]
handler404 = 'personal.views.handler404'
handler500 = 'personal.views.server_error'