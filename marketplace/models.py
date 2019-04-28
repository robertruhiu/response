import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from separatedvaluesfield.models import SeparatedValuesField


class Job(models.Model):
    ENGAGEMENT_TYPE = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Freelance', 'Freelance'),
    )

    JOB_ROLE = (
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend  Developer', 'Backend  Developer'),
        ('Android  Developer', 'Android  Developer'),
        ('Graphic Designer', 'Graphic Designer'),
        ('IOS Developer', 'IOS Developer'),
        ('Data Scientist', 'Data Scientist'),
    )

    DEV_EXPERIENCE = (
        ('Entry', 'Entry'),
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Senior', 'Senior'),
    )
    company = models.CharField(max_length=300)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_role = models.CharField(max_length=30, choices=JOB_ROLE, default='Full Stack Developer')
    dev_experience = models.CharField(max_length=30, choices=DEV_EXPERIENCE, default='Mid-Level')
    engagement_type = models.CharField(max_length=30, choices=ENGAGEMENT_TYPE, default='Full-time')
    tech_stack = models.CharField(max_length=500)
    num_devs_wanted = models.IntegerField(default=1)
    location = CountryField(null=True, max_length=30)
    remuneration = models.CharField(max_length=45, help_text='in dollars ($)')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    position_filled = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='job_applications', on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devs')
    selected = models.BooleanField(default=False)


class DevRequest(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    developers = SeparatedValuesField(null=True,max_length=150,token=',')
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)



    def amount(self):
        total_amount = 0
        total_devs = len(self.developers)

        if 1 <= total_devs <= 10:
            total_amount = 100
        elif 10 < total_devs <= 100:
            total_amount = 20 * total_devs
        return total_amount
