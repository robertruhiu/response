from django import forms
from django.forms import ModelForm, Form
from frontend.models import candidatesprojects,Portfolio,Github,Experience
from projects.models import Framework, Project
from django_countries.fields import CountryField


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
    image = forms.CharField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=True)
    demo_link = forms.CharField(required=True)
    repository_link = forms.CharField(required=True)
    class Meta:
        model = Portfolio
        fields = ['image','title','description','demo_link','repository_link']

class Github_form(Form):
    github_username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


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
