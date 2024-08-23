from unicodedata import name
from django.urls import path
from .views import (
    like_comment_view,
    dislike_comment_view,
    reply_to_comment_view,

)

app_name = 'comment'
urlpatterns = [
    path('like-comment/<username>/<book>/<text>/<comment_user>', like_comment_view, name = 'like-comment'),
    path('dislike-comment/<username>/<book>/<text>/<user>', dislike_comment_view, name = 'dislike-comment'),
    path('reply/<book_pk>/<comment_pk>/', reply_to_comment_view, name = 'reply')
]