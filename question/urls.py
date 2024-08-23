from django.urls import path
from .views import post_question_view, answer_view

app_name = 'question'

urlpatterns = [
    path('', post_question_view, name = 'question'),
    path('answer/', answer_view, name = 'answer'),
]