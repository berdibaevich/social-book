
from django.db import models
from account.models import Account
from book.models import Book

# Create your models here.





class ChatOnetoOne(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_user')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body





class DiscussBook(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner_of_disscus')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_for_disscus')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='sender_text')
    discussion_users = models.ManyToManyField(Account, related_name='all_users')
    when = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)
    is_ready = models.BooleanField(default=False) #when add time then is_ready will be True
    is_start = models.BooleanField(default=False) #when time is 0 the chat start


    
    class Meta:
        ordering = ['-updated']


    
    def __str__(self):
        return self.book.name






class ChatText(models.Model):
    room = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text







