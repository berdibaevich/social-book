from django import forms
from .models import MyAccount
from account.models import Account


class MyAccountForm(forms.ModelForm):

    class Meta:
        model = MyAccount
        fields = [
            'first_name',
            'last_name',
            'status',
            'social_telegram',
            'social_instagram',
            'social_facebook',
            'bio'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
        for f in self.fields:
            self.fields[str(f)].label = ''
            self.fields[str(f)].widget.attrs.update({'class': 'form-control', 'placeholder': f'{f}....'})



    











class MyImageForm(forms.ModelForm):
    profile_img = forms.ImageField(
        label= ""
        )
    
    class Meta:
        model = Account
        fields = ['profile_img']