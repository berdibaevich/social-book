from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Answer, Question


# Create your views here.


# question
def post_question_view(request):
    user = request.user
    if request.method == 'POST':
        question = request.POST.get('question')
        if question != '':
            Question.objects.create(
                user = request.user,
                question = question

            )


        return redirect('/')








#answer
def answer_view(request):
    user = request.user
    if request.method == 'POST':
        question_pk = request.POST.get('question')
        answer = request.POST.get('answer')
        question = Question.objects.get(pk = question_pk)
        if answer != '':
            obj = Answer.objects.create(
                user = user,
                question = question,
                answer = answer,
            )
            question.is_answered = True
            question.save()

            



        else:
            messages.warning(request, 'It is not answer this question!')
            return redirect('/')


        return redirect('/')

    
    