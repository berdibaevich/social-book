from django import forms
from .models import Book



class BookForm(forms.ModelForm):
    language = forms.CharField(
        label='',
        help_text= '<small class="helptext mb-0 ms-4 text-muted">Kr-Uz-Eng-Rus tillerinin\' birewin kiritesiz</small>',#'Kr,Uz,Eng,Rus tillerinin\' birewin kiritesiz',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Kitap qaysi tilde jazilg\'anin kiritin...'
            }

        )
    )
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kitaptin\' ati...'
            }
        )
    )

    subtitle = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kitap haqida qisqasha muzmuni...',
                'rows': 3
            }
        )
    )

    author = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kitap avtori...',
            }
        )
    )



    feedback = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': "Ozin'iz qisqasha pikir kiritin' usi kitap haqida...",
                'rows': 4
            }
        )
    )


    class Meta:
        model = Book
        fields = ('language', 'name', 'subtitle', 'author', 'image', 'feedback')
  

