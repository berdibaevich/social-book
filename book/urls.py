from django.urls import path
from .views import (
    book_detail_view,
    delete_book_view,
    star_rating_view,
    add_book,
    update_book_function,
    delete_book_view,
)


app_name = 'book'

urlpatterns = [
    path('<int:pk>/', book_detail_view, name = 'detail'),
    path('rating', star_rating_view, name = 'rating'),
    path('add-book/', add_book, name = 'add-book'),
    path('update/<book>/', update_book_function, name = 'update'),
    path('delete/<book>/', delete_book_view, name = 'delete'),
    

]