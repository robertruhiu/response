from django.contrib.auth.models import User
from django.db import models


from projects.models import Language, Framework ,Project
from transactions.models import Transaction


# Create your models here.
class candidatesprojects(models.Model):
    stage = models.CharField(default='awaiting candidate', max_length=100)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


class devs(models.Model):
    email=models.EmailField(null=True,max_length=50)
    language=models.CharField(null=True,max_length=500)
    framework=models.CharField(null=True,max_length=500)
    country =models.CharField(null=True,max_length=30)
    firstname=models.CharField(null=True,max_length=30)
    lastname=models.CharField(null=True,max_length=30)
    github = models.CharField(null=True,max_length=500)
    linkedin = models.CharField(null=True, max_length=500)
    portfolio = models.CharField(null=True, max_length=500)

class recruiters(models.Model):
    email = models.EmailField(null=True,max_length=50)
    country = models.CharField(null=True,max_length=30)
    firstname = models.CharField(null=True,max_length=30)
    lastname = models.CharField(null=True,max_length=30)
    company = models.CharField(null=True,max_length=200)
    companyurl = models.CharField(null=True,max_length=200)
