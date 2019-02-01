from django import forms
from django.forms import ModelForm, Form
from frontend.models import candidatesprojects
from projects.models import Framework, Project


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
