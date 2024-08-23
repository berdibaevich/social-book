from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import pathlib
import uuid

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError('Users must be have an email address')

        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)

        return user




def profile_img(instance, filename):
    path = pathlib.Path(filename)
    new_path = str(uuid.uuid4)
    return f"profile_image/{new_path}{path.suffix}"



class Account(AbstractBaseUser):
    username = models.CharField(max_length=60)
    email = models.EmailField(unique=True, max_length=60)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_img = models.ImageField(default = 'no.jpg', upload_to = profile_img)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj = None):
        return self.is_admin


    
    def has_module_perms(self, app_label):
        return True




    #this method help us how many messages do i have
    def get_count_message(self):
        message = self.to_user.all().filter(is_read = False)
        if message.exists():
            return message.count()

        return False
