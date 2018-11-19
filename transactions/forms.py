from django import forms
from transactions.models import Candidate, Transaction

from django.forms import ModelForm, Form


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        exclude = ('transaction',)


class SourcingForm(Form):
    job_roles = (
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend  Developer', 'Backend  Developer'),
        ('Android Developer', 'Android  Developer'),
        (' Graphic Designer', 'Graphic Designer'),
        ('IOS  Developer', 'IOS Developer'),
        ('Data Scientist', 'Data Scientist'),
    )
    job_role = forms.ChoiceField(choices=job_roles)
    engagement = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
    )
    email_address = forms.EmailField(required=True)
    phone_number = forms.IntegerField()
    name = forms.CharField(max_length=255)
    company_name = forms.CharField(max_length=255)
    tech_stack = forms.CharField(max_length=255)
    Number_of_devs_needed = forms.IntegerField()
    renumeration_in_dollars = forms.IntegerField()

