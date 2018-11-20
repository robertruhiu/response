from django import forms

from projects.models import Framework
def framework_choices():
    return tuple([(str(framework.name).lower(), framework.name) for framework in Framework.objects.all()])

class FrameworkForm(forms.Form):
    name = forms.ChoiceField(choices=framework_choices)
