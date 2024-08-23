from django.db import models
from account.models import Account

# Create your models here.




class Question(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='question_user')
    question = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    



    def __str__(self):
        return self.question





class Answer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answer_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return self.answer



