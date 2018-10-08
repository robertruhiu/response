from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, DateInput, TextInput, Select, EmailInput, RadioSelect, FileInput, \
    SelectMultiple
from django.utils.translation import ugettext_lazy as _
from .models import *


class ProfileTypeForm(forms.Form):
    USER_TYPE_CHOICES = (
        ('recruiter', 'RECRUITER'),
        ('developer', 'DEVELOPER'),
    )
    profile_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)


class DeveloperFillingDetailsForm(forms.Form):
    PROGRAMMING_LANGUAGE_CHOICES = (('python', 'Python'),)
    FRAMEWORK_CHOICES = (('django', 'Django'),)
    YEARS_ACTIVE_CHOICES = (
        ('1-2', '1-2'),
        ('2-4', '2-4'),
        ('4-above', '4-above'),
    )
    github_repo = forms.URLField(help_text='Example: https://www.github.com/username')
    programming_languages = forms.MultipleChoiceField(choices=PROGRAMMING_LANGUAGE_CHOICES)
    frameworks = forms.MultipleChoiceField(choices=FRAMEWORK_CHOICES)
    years = forms.ChoiceField(choices=YEARS_ACTIVE_CHOICES)

class RecruiterFillingDetailsForm(forms.Form):
    company = forms.CharField(max_length=140)
    job_role = forms.CharField(max_length=140)
    industry = forms.CharField(max_length=80)
    staff_size = forms.IntegerField()
    company_url = forms.URLField()

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Philisiah'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Mwaluma'}))
    field_order = [
        'first_name',
        'last_name',
        'email',
    ]

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', }),
            'last_name': TextInput(attrs={'class': 'input', }),
            'email': EmailInput(attrs={'class': 'input', 'type': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'profile_photo': FileInput(attrs={'class': 'file-input', }),
        }
