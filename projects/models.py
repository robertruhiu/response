from django.contrib.auth.models import User
from django.db import models

from testing.models import Snapshot


# Create your models here.

# TODO: add model for category to classify all projects using project category, can be multiple ie frontend, backend
# TODO: categorise language into frontend, backend etc


class Language(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Framework(models.Model):
    name = models.CharField(max_length=140)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name= 'language', null=True)
    framework = models.ForeignKey(Framework, on_delete=models.SET_NULL, related_name='framework',null=True)
    snapshot = models.ForeignKey(Snapshot, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name
