from django.test import TestCase
from .models import Question, Answer
from account.models import Account
from django.urls import reverse, resolve
from .views import post_question_view, answer_view
# Create your tests here.



class QuestionAndAnswerTest(TestCase):
    def setUp(self) -> None:

        self.user1 = Account.objects.create(
            username = 'user1',
            email = 'u@gmail.com',
            password = 'admin'
        )

        self.user2 = Account.objects.create(
            username = 'user2',
            email = 'u@a.com',
            password = 'secret'
        )


        self.question = Question.objects.create(
            user = self.user1,
            question = 'I need some'
        )


    
    def test_question_model_str(self):
        question = str(self.question)
        self.assertEqual(question, 'I need some')

        self.assertNotEqual(self.question.is_answered, True)


    
    def test_answer_model(self):
        answer = Answer.objects.create(
            user = self.user2,
            question = self.question,
            answer = 'That is'
        )

        self.question.is_answered = True
        self.question.save()

        self.assertEqual(str(answer), 'That is')

        self.assertEqual(self.question.is_answered, True)







class QuestionAndAnswerTemplateViewTest(TestCase):
    def setUp(self) -> None:

        self.user1 = Account.objects.create(
            username = 'user1',
            email = 'u@gmail.com',
            password = 'admin'
        )

        self.question = Question.objects.create(
            user = self.user1,
            question = 'I need some'
        )


    def test_question_template_func_view(self):

        url = reverse('question:question')
        self.assertEqual(resolve(url).func,post_question_view)

        

     