from django.core.exceptions import ValidationError

languages = ['Kr', 'Eng', 'Rus', 'Uz']


def validate_language(value):
    if value.title() not in languages:
        raise ValidationError(f"{value} qayte! Usilardan ['Kr', 'Eng', 'Rus', 'Uz'] birin kiritin.")

        