from django.db import models
from account.models import Account
from django.db.models import Count, Sum
from .validators import validate_language
# Create your models here.




class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)


    def __str__(self):
        return self.title

    # TOMENDEGI PROPERTY METHOD OTE JAMAN SEBEBI HITS TO DB 
    # @property
    # def count_book(self):
    #     #return self.tag_of_book.all().count()
    #     return len(self.tag_of_book.all())




class Book(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="owner_of_book")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True, related_name="tag_of_book")
    language = models.CharField(max_length=5, validators=[validate_language])
    name = models.CharField(max_length=200)
    subtitle = models.TextField()
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'book_image')
    audio = models.FileField(upload_to='book_audio', null=True, blank=True)
    feedback = models.CharField(max_length=200)
    views = models.ManyToManyField(Account, related_name='views', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_saved = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.owner.username}.Book is {self.name} and Tag is {self.tag.title}"


    class Meta:
        ordering = ['-created', '-updated']




    #get comment how many
    def get_comment(self):
        return self.parentcomment_set.filter(parent=None).count()


    #get reading count
    def get_reading_count(self):
        reading = self.reading.all().first()
        if reading is not None:
            return reading.count

        return 0


    #get already readed
    def get_readed(self):
        readed = self.readed.all().first()
        if readed is not None:
            return readed.count
        return 0





    #get_wil_read
    def get_willread(self):
        will_read = self.will_read.all().first()
        if will_read is not None:
            return will_read.count
        return 0


    #get discuss about book

    def get_discuss(self):
        discuss = self.discuss.all().first()
        if discuss is not None:
            return discuss.count
        
        return 0




    # define like or not
    def get_like_or_not(self, user):
        like = self.like_book.prefetch_related("users").all().first()
        if user in like.users.all():
            return True
        return False


    # define dislike or not
    def get_dislike_or_not(self, user):
        dislike = self.dislike_book.prefetch_related("users").all().first()
        if user in dislike.users.all():
            return True
        return False



    def get_like_counter(self):
        like = self.like_book.prefetch_related("users").all().first()
        return like.users.all().count()


    





    def get_star_users_count(self):
        star = self.book_star.all()
        if star.exists():
            users = []
            for i in star:
                for user in i.users.all():
                    if user:
                        users.append(1)
            return sum(users)
        
        return 0





    def get_star_protsent(self):
        if self.get_star_users_count():
            get_how_many = self.get_star_users_count() * 0.1
            return get_how_many + 1
        return 0





    def count_views(self):
        return self.views.all().count()
        


    




    def get_score(self, user):
        if self.book_rating.select_related("user").filter(user = user).exists():
            return self.book_rating.select_related("user").filter(user = user).first()
        return False


    
    def get_rating(self, user):
        return self.book_rating.select_related("user").filter(user = user).first()






    #this method gives us how many users which is entered one of them a diffirent rating
    def get_filter_users(self, star):
        get_star = self.book_star.all().filter(star = star).first()
        # users = [user for user in get_star.users.all()] or None
        users = get_star.users.all().count() or None
        if users is not None:
            return users
        return 0


    # NEW METHOD FOR RATING STAR GET
    def get_percentage_of_star(self):
        # obj = self.book_star.aggregate(Sum('percentage_of_score'))['percentage_of_score__sum'] or 0
        # return obj
        obj = self.book_star.all()
        if obj:
            return sum([x.percentage_of_score for x in obj]) 
        return 0

    

    def get_users_of_star(self):
        return int(self.get_percentage_of_star() * 10)



    def get_filter_star_(self, star):
        star = self.book_star.filter(star = star).first() or None
        return star

    
    
    def get_five_of_star(self):
        if hasattr(self, '_five_of_star'):
            return self._five_of_star
        star = self.book_star.select_related('book').filter(star=5).first()
        if star:
            self._five_of_star = star.percentage_of_score
        else:
            self._five_of_star = 0
        return self._five_of_star



    # def get_five_of_star(self):
    #     obj = self.get_filter_star_(5)
    #     if obj:
    #         return obj.percentage_of_score
    #     return 0


    def get_four_of_star(self):
        obj = self.get_filter_star_(4)
        if obj:
            return obj.percentage_of_score
        return 0


    def get_three_of_star(self):
        obj = self.get_filter_star_(3)
        if obj:
            return obj.percentage_of_score
        return 0


    def get_two_of_star(self):
        obj = self.get_filter_star_(2)
        if obj:
            return obj.percentage_of_score
        return 0


    def get_one_of_star(self):
        obj = self.get_filter_star_(1)
        if obj:
            return obj.percentage_of_score
        return 0




    def get_five_of_star_for_style_width(self):
        obj = self.get_filter_star_(5)
        if obj:
            return int(obj.percentage_of_score * 10)
        return 0



    def get_four_of_star_for_style_width(self):
        obj = self.get_filter_star_(4)
        if obj:
            return int(obj.percentage_of_score * 10)
        return 0



    def get_three_of_star_for_style_width(self):
        obj = self.get_filter_star_(3)
        if obj:
            return int(obj.percentage_of_score * 10)
        return 0



    def get_two_of_star_for_style_width(self):
        obj = self.get_filter_star_(2)
        if obj:
            return int(obj.percentage_of_score * 10)
        return 0



    def get_one_of_star_for_style_width(self):
        obj = self.get_filter_star_(1)
        if obj:
            return int(obj.percentage_of_score * 10)
        return 0

    # END NEW METHOD FOR RATING STAR GET






class Star(models.Model):
    CHOICE_STAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_star')
    star = models.IntegerField(choices=CHOICE_STAR, default=0)
    users = models.ManyToManyField(Account, related_name='star_users', blank=True)
    percentage_of_score = models.DecimalField(max_digits=5, decimal_places=1, default=0)


    def __str__(self):
        return f"{self.book.name} -- {self.star}"







class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_rating')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='rating_user')
    score = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user.username} -- {self.score}"









