from django.contrib import admin
from .models import Readed, WillRead, Reading, Discuss

# Register your models here.


admin.site.register([WillRead, Reading, Readed, Discuss])