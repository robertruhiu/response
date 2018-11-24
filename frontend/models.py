from django.contrib.auth.models import User
from django.db import models


from projects.models import Language, Framework ,Project
from transactions.models import Transaction


# Create your models here.
class candidatesprojects(models.Model):
    stage = models.CharField(default='awaiting candidate', max_length=100)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)


