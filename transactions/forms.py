from django import forms
from transactions.models import Candidate, Transaction
from django_countries.fields import CountryField
from django.forms import ModelForm, Form
from phonenumber_field.modelfields import PhoneNumberField


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
    contract = forms.ChoiceField(choices=engagement,required=True)
    email_address = forms.EmailField(required=True)
    phone_number = PhoneNumberField().formfield(required=True)
    name = forms.CharField(max_length=255,required=True)
    company_name = forms.CharField(max_length=255,required=True)
    tech_stack = forms.CharField(max_length=255,required=True)
    Number_of_devs_needed = forms.IntegerField(required=True)
    renumeration_in_dollars = forms.CharField(required=True)
    country = CountryField().formfield(required=True)

