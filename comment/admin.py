from django.contrib import admin
from .models import ParentComment, ChildComment


# Register your models here.


admin.site.register(ParentComment)
admin.site.register(ChildComment)