from django.contrib import admin
from .models import Tag, Book, Star, Rating


# Register your models here.



admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Star)