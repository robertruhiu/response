from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# TODO: add model for category to classify all projects using project category, can be multiple ie frontend, backend
# TODO: categorise language into frontend, backend etc


class Language(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Framework(models.Model):
    name = models.CharField(max_length=140)
    language = models.ForeignKey(Language, on_delete=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=False)
    description = models.CharField(max_length=200, blank=True, null=True, )
    framework = models.ForeignKey(Framework, on_delete=False, null=True)

    def __str__(self):
        return self.name
