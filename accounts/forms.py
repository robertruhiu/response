from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, DateInput, TextInput, Select, EmailInput, RadioSelect, FileInput, \
    SelectMultiple
from django.utils.translation import ugettext_lazy as _
from accounts.models import Profile


class ProfileTypeForm(forms.Form):
    USER_TYPE_CHOICES = (
        ('recruiter', 'RECRUITER'),
        ('developer', 'DEVELOPER'),
    )
    profile_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)


class DeveloperFillingDetailsForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows': 7}))
    class Meta:
        model = Profile

        fields = ['github_repo','gender','phone_number', 'linkedin_url',
                  'portfolio','years','country','language', 'framework','availabilty','csa','about']


    # PROGRAMMING_LANGUAGE_CHOICES = (('python', 'Python'),)
    # FRAMEWORK_CHOICES = (('django', 'Django'),)
    # YEARS_ACTIVE_CHOICES = (
    #     ('1-2', '1-2'),
    #     ('2-4', '2-4'),
    #     ('4-above', '4-above'),
    # )
    # github_repo = forms.URLField(help_text='Example: https://www.github.com/username')
    # programming_languages = forms.MultipleChoiceField(choices=PROGRAMMING_LANGUAGE_CHOICES)
    # frameworks = forms.MultipleChoiceField(choices=FRAMEWORK_CHOICES)
    # years = forms.ChoiceField(choices=YEARS_ACTIVE_CHOICES)

class RecruiterFillingDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ['company', 'job_role', 'industry', 'country','company_url']

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': ''}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': ''}))
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
        fields = ('first_name', 'last_name',)
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', }),
            'last_name': TextInput(attrs={'class': 'input', })

        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'stage', )
        widgets = {
            'profile_photo': FileInput(attrs={'class': 'file-input', }),
        }

class DeveloperProfileEditForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows': 7}))
    class Meta:
        model = Profile
        fields = ['github_repo','phone_number', 'linkedin_url',
                  'portfolio','language', 'framework','availabilty','csa','about']

class RecruiterProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'job_role', 'industry', 'company_url','country']
