from django.db import models
from book.models import Book
from account.models import Account

# Create your models here.




class ParentComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='comment_likes')
    dislikes = models.ManyToManyField(Account, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='parents_comment')

    def __str__(self):
        return self.text

    # get all children from parent comment
    @property
    def children(self):
        return ParentComment.objects.filter(parent = self).order_by('-created').all()
    
    #define parent is none texts
    @property
    def is_parent(self):
        if self.parent is None:
            return True

        return False


    def get_children_count(self):
        children = ParentComment.objects.filter(parent = self)
        if children.exists():
            return children.count()
        
        return 0
        


    


    #get like comment counter as 10k
    def get_comment_counter(self):
        comment = self.comment_likes.all().first()
        if comment:
            return comment.counter

        return 0



    #get like it or not 
    def get_liked_it(self):
        return self.likes.all()


    #get dislike
    def get_dislike_it(self):
        return self.dislikes.all()






class ChildComment(models.Model):
    parent = models.ForeignKey(ParentComment, on_delete=models.CASCADE, related_name='parent_comment')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='parent_comment_user')
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)












        