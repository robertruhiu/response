from django.db import models
from django.contrib.auth.models import User
from projects.models import Project, Framework


# Create your models here.
class Transaction(models.Model):
    # TODO: allow user to specify framework for test

    STAGE_CHOICES = (
        ('created', 'created'),
        ('upload-candidates', 'upload-candidates'),
        ('payment-stage', 'payment-stage'),
        ('make-payment', 'make-payment'),
        ('payment-confirmed', 'payment-confirmed'),
        ('payment-verified', 'payment-verified'),
        ('complete', 'complete'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stage = models.CharField(choices=STAGE_CHOICES, default='created', max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)

    def allcandidates(self):
        candidates = Candidate.objects.filter(transaction=self.id)
        return candidates

    def amount(self):
        if self.allcandidates().count() <= 10:
            total_amount = 200
        elif self.allcandidates().count() > 10 and self.allcandidates().count() <= 50:
            total_amount = 20 * self.allcandidates().count()
        return total_amount

    def __str__(self):
        return "{},{},{}".format(self.user.username, self.project.name, self.stage)


class Candidate(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def generate_link(self):
        pass

    def generate_temporary_password(self):
        pass

    def __str__(self):
        return "{}, {}".format(self.first_name, self.last_name)
class OpenCall(models.Model):
    recruiter =models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    transaction =models.IntegerField()


class Applications(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recruiter')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE,related_name='developer')
    stage = models.CharField(default='requirements met', max_length=100)
    transaction = models.IntegerField()
    score = models.IntegerField()
