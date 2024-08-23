from django.urls import path
from .views import (
    my_account_view,
    edit_my_account_view,
    follow_view,
    save_book,

)

app_name = 'myaccount'


urlpatterns = [
    path('<int:pk>/', my_account_view, name = 'my-account'),
    path('<int:pk>/edit/',edit_my_account_view, name = 'edit'),
    path('<int:pk>/follow/',follow_view, name = 'follow'),
    path('save/<user>/<book>/', save_book, name = 'save'),

]