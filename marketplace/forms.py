from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('posted_by', 'created', 'updated', 'position_filled',)
