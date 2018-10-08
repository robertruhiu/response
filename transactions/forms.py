from django import forms
from transactions.models import Candidate, Transaction

from django.forms import ModelForm

class CandidateForm(ModelForm):

    class Meta:
        model = Candidate
        exclude = ('transaction',)
