from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm

# registerForm
class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')



    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


        for f in self.fields:
            self.fields[str(f)].label = ''
            self.fields[str(f)].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password...' if f == 'password1' else f"{f.title()}..."})
    



    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            account = Account.objects.get(email = email)
        
        except Exception as e:
            return email

        raise forms.ValidationError(f"Email {email} already in use")





    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            account = Account.objects.get(username = username)
        
        except Exception as e:
            return username

        raise forms.ValidationError(f"Username {username} already in use")

# /registerForm



