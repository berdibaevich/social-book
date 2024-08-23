from django.db import models
from book.models import Book
from account.models import Account
from comment.models import ParentComment




# Create your models here.


class Like(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="like_book", null=True, blank=True)
    comment = models.ForeignKey(ParentComment, on_delete=models.CASCADE, related_name='comment_likes', null=True, blank=True)
    users = models.ManyToManyField(Account, related_name='like_users')
    counter = models.IntegerField(default=0)



    def __str__(self):
        return str(self.counter)
        








class Dislike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="dislike_book", null=True, blank=True)
    comment = models.ForeignKey(ParentComment, on_delete=models.CASCADE, related_name='comment_dislikes', null=True, blank=True)
    users = models.ManyToManyField(Account, related_name='dislike_users')
    counter = models.IntegerField(default=0)



    def __str__(self):
        return str(self.counter)