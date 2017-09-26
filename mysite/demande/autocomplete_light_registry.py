import autocomplete_light.shortcuts as al
from django.contrib.auth.models import User
from .models import Task

#https://github.com/yourlabs/django-autocomplete-light
# This will generate a PersonAutocomplete class

al.register(User,
    search_fields=['username', 'email',],
    choices=User.objects.all(),
    attrs={
        'placeholder': 'Ajouter un auteur ?',
        'data-autocomplete-minimum-characters': 2,
    },
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 1,
        'class': 'modern-style',
    },
)