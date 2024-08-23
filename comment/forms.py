from django import forms
from .models import ChildComment, ParentComment



class ParentCommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder': 'Add a comment...',
                'rows': 2
            }
        )
    )
    class Meta:
        model = ParentComment
        fields = ('text',)









class ChildCommentForm(forms.ModelForm):
    text = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder': 'replies a comment...',
            }
        )
    )
    class Meta:
        model = ChildComment
        fields = ('text',)