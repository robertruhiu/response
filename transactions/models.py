from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


# Create your models here.
class Transaction(models.Model):
    # TODO: allow user to specify framework for test

    STAGE_CHOICES = (
        ('upload_candidate', 'upload_candidate'),
        ('payment_stage', 'payment_stage'),
        ('payment_verified', 'payment_verified'),
        ('send_credentials', 'send_credentials'),
        ('complete', 'complete'),
    )
    user = models.ForeignKey(User, on_delete=False)
    project = models.ForeignKey(Project, on_delete=False)
    stage = models.CharField(choices=STAGE_CHOICES, default='upload_candidate', max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=False)
    completed = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "{},{},{}".format(self.user.username, self.project.name, self.created, self.stage)


class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    transaction = models.ForeignKey(Transaction, on_delete=False)

    def generate_link(self):
        pass

    def generate_temporary_password(self):
        pass

    def __str__(self):
        return self.names
