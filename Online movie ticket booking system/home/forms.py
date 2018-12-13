from django import forms
from django.contrib.auth.models import User

from .models import *


class TheatreForm(forms.ModelForm):
    class Meta:
        model = Theatre
        fields = ['theatre_name', 'city']
