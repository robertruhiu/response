from django import forms
from django.forms import ModelForm, Form
from frontend.models import candidatesprojects


class Projectinvite(forms.ModelForm):
    stage = forms.CharField(required=True)
    transaction = forms.IntegerField(required=True)
    candidate = forms.IntegerField(required=True)

    class Meta:
        model = candidatesprojects
        fields=['stage','transaction','candidate']

