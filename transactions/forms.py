from django import forms
from django.forms import ModelForm, Form
from django_countries import Countries
from phonenumber_field.formfields import PhoneNumberField
from accounts.models import Profile
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
    tech_stack = forms.CharField(max_length=255, required=True)
    number_of_devs_needed = forms.IntegerField(required=True)
    renumeration_in_dollars = forms.CharField(required=True)



