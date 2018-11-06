from django import forms
from transactions.models import Candidate, Transaction

from django.forms import ModelForm, Form

class CandidateForm(ModelForm):

    class Meta:
        model = Candidate
        exclude = ('transaction',)

class SourcingForm(Form):
    email_address = forms.EmailField(required=True)
    phone_number = forms.NumberInput()
    name = forms.CharField(max_length=255)
    company_name = forms.CharField(max_length=255)
    job_role = forms.MultipleChoiceField()
    engagement_types = forms.MultipleChoiceField()
    tech_stack = forms.CharField(max_length=255)
    project_description = forms.TextInput()
    devs_needed = forms.NumberInput()
    renumeration = forms.NumberInput()
    tech_staff = forms.ChoiceField()
    skills_test =  forms.ChoiceField()
