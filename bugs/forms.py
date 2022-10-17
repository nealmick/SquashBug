from django import forms
from .models import Bug


class BugUpdateForm(forms.ModelForm):

    class Meta:
        model = Bug
        fields = ['title', 'description']