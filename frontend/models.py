from django.contrib.auth.models import User
from django.db import models

from marketplace.models import Job
from django_countries.fields import CountryField
from projects.models import Language, Framework ,Project
from transactions.models import Transaction
from separatedvaluesfield.models import SeparatedValuesField

# Create your models here.
class candidatesprojects(models.Model):
    stage = models.CharField(default='awaiting candidate', max_length=100)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE,null=True,)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,null=True,)




class submissions(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    demo = models.CharField(null=True, max_length=400)
    repo = models.CharField(null=True, max_length=400)

class Portfolio(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=200)
    description = models.CharField(null=True, max_length=400)
    repository_link = models.CharField(null=True, max_length=400)
    demo_link = models.CharField(null=True, max_length=400)
    verified = models.BooleanField(default=False)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )


class Experience(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=True, max_length=100)
    company = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=100)
    location = CountryField(null=True, max_length=30)
    duration = models.IntegerField(null=True)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )

class Report(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    requirements= SeparatedValuesField(null=True,max_length=150,token=',')
    keycompitency = SeparatedValuesField(null=True,max_length=150,token=',')
    grading = SeparatedValuesField(null=True,max_length=150,token=',')
    score = models.IntegerField(null=True)
    github = models.CharField(null=True, max_length=300)





