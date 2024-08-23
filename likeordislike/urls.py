from django.urls import path
from .views import (
    like_view,
    dislike_view,

)


app_name = 'likeordislike'

urlpatterns = [
    path('like/<username>/<book>/', like_view, name = 'like'),
    path('dislike/<username>/<book>/', dislike_view, name = 'dislike'),

]