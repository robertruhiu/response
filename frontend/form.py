from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User

from frontend.models import candidatesprojects,Portfolio,Experience
from projects.models import Framework, Project
from django_countries.fields import CountryField
from accounts.models import Profile
from cloudinary.forms import  CloudinaryFileField


class Projectinvite(forms.ModelForm):
    stage = forms.CharField(required=True)
    transaction = forms.IntegerField(required=True)
    candidate = forms.IntegerField(required=True)

    class Meta:
        model = candidatesprojects
        fields = ['stage', 'transaction', 'candidate']
class Submissions(Form):
    repositorylink=forms.CharField(required=True)
    demolink=forms.CharField(required=True)
class Experience_Form(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=True)
    duration = forms.IntegerField(required=True)
    company = forms.CharField(required=True)

    class Meta:
        model = Experience
        fields=['title','description','location','company','duration']
class Portfolio_form(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=True)
    demo_link = forms.CharField(required=True)
    repository_link = forms.CharField(required=True)
    class Meta:
        model = Portfolio
        fields = ['title','description','demo_link','repository_link']


class GradingForm(Form):
    REQUIREMENT_TYPE_CHOICES = (
        ('complete', 'COMPLETE'),
        ('partial', 'PARTIAL'),
        ('incomplete', 'INCOMPLETE'),
    )
    github = forms.CharField(required=False)
    score = forms.IntegerField(required=False)
    requirement1 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement2 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement3 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement4 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement5 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement6 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement7 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement8 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement9 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    requirement10 = forms.ChoiceField(choices=REQUIREMENT_TYPE_CHOICES)
    deliverables = forms.IntegerField(required=False)
    errors = forms.IntegerField(required=False)
    security = forms.IntegerField(required=False)
    readability = forms.IntegerField(required=False)
    passed = forms.IntegerField(required=False)
    failed = forms.IntegerField(required=False)
    vulnerable =forms.IntegerField(required=False)
    lines = forms.IntegerField(required=False)
    duplications = forms.IntegerField(required=False)
    classes = forms.IntegerField(required=False)
    comments = forms.IntegerField(required=False)
    depedencies = forms.IntegerField(required=False)
    debt = forms.CharField(required=False)
    gates = forms.CharField(required=False)


class About(forms.ModelForm):

    about = forms.CharField(widget=forms.Textarea(attrs={'rows': 7}), required=True)
    class Meta:
        model =Profile
        fields =['about']
class EditProjectForm(forms.ModelForm):
    name = forms.CharField()
    brief = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    projectimage1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    projectimage2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    projectimage3 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage4 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage5 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage6 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage7 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage8 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage9 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    projectimage10 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    requirement2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    requirement3 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    requirement4 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), )
    requirement5 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement6 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement7 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement8 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement9 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    requirement10 = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)


    class Meta:
        model = Project

        fields = ['name', 'description', 'level', 'projectimage1', 'projectimage2', 'projectimage3', 'projectimage4',
                  'projectimage5', 'projectimage6', 'projectimage7', 'projectimage8', 'projectimage9', 'projectimage10',
                  'requirement1', 'requirement2', 'requirement3', 'requirement4', 'requirement5', 'requirement6',
                  'requirement7', 'requirement8', 'requirement9', 'requirement10', 'framework','devtype','projecttype','owner','brief','hasvideo']
class CvForm(ModelForm):
    file = CloudinaryFileField(
        options={
            'resource_type': "raw"
        })
    class Meta:
        model = Profile
        fields=['file']
