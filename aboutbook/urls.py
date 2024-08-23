from django.urls import path
from .views import (
    reading_book_view,
    readed_book_view,
    will_read_book_view,
    discuss_view,

)

app_name = 'aboutbook'

urlpatterns = [
    path('reading/<user>/<book_name>/', reading_book_view, name = 'reading'),
    path('readed/<user>/<book_name>/', readed_book_view, name = 'readed'),
    path('read/<user>/<book_name>/', will_read_book_view, name = 'will_read'),
    path('discuss/<user>/<book_name>/', discuss_view, name = 'discuss'),

]