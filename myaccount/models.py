from django.db import models
from account.models import Account
from django.db.models.signals import post_save
from django.dispatch import Signal
from book.models import Book
# Create your models here.



class MyAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    status = models.CharField(max_length=50, help_text="Ozinizdin' jonelisin'izdi kiritin!")
    social_telegram = models.CharField(max_length=60, null=True, blank=True)
    social_instagram = models.CharField(max_length=60, null=True, blank=True)
    social_facebook = models.CharField(max_length=60, null=True, blank=True)
    bio = models.TextField(null=True, blank=True, help_text="Ozin'iz haqqinda mag'liwmat!")
    friends = models.ManyToManyField(Account, blank=True, related_name='friends')
    favorites_book = models.ManyToManyField(Book, related_name='favorites_books', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    followers = models.IntegerField(default=0)


    
    def __str__(self):
        return self.account.username



    def get_saved_books(self):
        return self.favorites_book.all()







    





#Following class
class Follow(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    follower = models.ManyToManyField(Account, related_name='follower', blank=True)
    following = models.ManyToManyField(Account, related_name='following', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.username






def post_save_account(sender, instance, created, **kwargs):
    if created:
        MyAccount.objects.create(
            account = instance
        )






Signal.connect(post_save, post_save_account, sender=Account)







  