from django.db import models
from account.models import Account
from book.models import Book


# Create your models here.




class WillRead(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='will_read')
    users = models.ManyToManyField(Account, related_name='user_of_willread')
    count = models.IntegerField(default=0)



    def __str__(self):
        return self.book.name



class Reading(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading')
    users = models.ManyToManyField(Account, related_name='user_of_reading')
    count = models.IntegerField(default=0)


    def __str__(self):
        return self.book.name



class Readed(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='readed')
    users = models.ManyToManyField(Account, related_name='user_of_readed')
    count = models.IntegerField(default=0)



    def __str__(self):
        return self.book.name




class Discuss(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='discuss')
    users = models.ManyToManyField(Account, related_name='user_of_discuss')
    count = models.IntegerField(default=0)



    def __str__(self):
        return f'{self.book.name} - {str(self.count)}'



