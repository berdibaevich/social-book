from django.urls import path
from .views import (
    send_message_view,
    get_message_from_js,
    create_room,
    start_discuss,
    start_is_true_view,
    rooom,
    close_chat_view,

)


app_name = 'chat'

urlpatterns = [
    path('', send_message_view, name = 'chat'),
    path('message/', get_message_from_js, name = 'message'),
    path('create-room/', create_room, name = 'create-room'),
    path('start-discuss', start_discuss, name = 'start-discuss'),
    path('start_time/', start_is_true_view, name = 'start-time'),
    path('room/<room>', rooom, name = 'room'),
    path('close/<room_name>', close_chat_view, name = 'close'),





]