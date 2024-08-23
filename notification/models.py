from django.db import models
from account.models import Account
from book.models import Book


# Create your models here.



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'LIKE'),
        (2, 'COMMENT'),
        (3, 'FOLLOW'),
        (4, 'MESSAGE'),
        (5, 'DISCUSS')

    )
    sender = models.ForeignKey(Account, related_name='sender', blank=True, null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='receiver')
    notification_types = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    message_text = models.CharField(max_length=100, blank=True, null=True)
    how_many = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default=False)

    #
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    


    def __str__(self):
        return f'receiver: {self.receiver.username} types is {self.notification_types}'





