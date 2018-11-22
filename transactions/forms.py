from django import forms
from django.forms import ModelForm, Form
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

from transactions.models import Candidate


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        exclude = ('transaction',)


def job_roles():
    return (
        (' Choose...',' Choose...'),        
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend  Developer', 'Backend  Developer'),
        ('Android Developer', 'Android  Developer'),
        (' Graphic Designer', 'Graphic Designer'),
        ('IOS  Developer', 'IOS Developer'),
        ('Data Scientist', 'Data Scientist'),
    )

def engagement():
    
    return (
        ('Choose...','Choose...'),
        ('Full-time', 'Full-time'),        
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
    )


class SourcingForm(Form):
    job_role = forms.ChoiceField(choices=job_roles)
    contract = forms.ChoiceField(choices=engagement, required=True)
    email_address = forms.EmailField(required=True)
    # phone_number = PhoneNumberField()
    name = forms.CharField(max_length=255, required=True)
    company_name = forms.CharField(max_length=255, required=True)
    tech_stack = forms.CharField(max_length=255, required=True)
    number_of_devs_needed = forms.IntegerField(required=True)
    renumeration_in_dollars = forms.CharField(required=True)
    country = forms.CharField(required=True)
    
