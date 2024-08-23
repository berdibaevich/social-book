from django.contrib import admin
from .models import Account

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_joined', 'last_login']
    search_fields = ['username', 'email']

    # class Meta:
    #     model = Account



admin.site.register(Account, AccountAdmin)