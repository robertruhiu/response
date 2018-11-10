from django.db import models

# Create your models here.
class Snapshot(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IpAddress(models.Model):
    ip = models.GenericIPAddressField()
    domain = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.domain
