from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
import datetime
from django.core.cache import cache
from separatedvaluesfield.models import SeparatedValuesField
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('recruiter', 'RECRUITER'),
        ('developer', 'DEVELOPER'),
    )
    STAGE_CHOICES = (
        ('profile_type_selection', 'profile_type_selection'),
        ('recuiter_filling_details', 'recuiter_filling_details'),
        ('developer_filling_details', 'developer_filling_details'),
        ('complete', 'complete'),
    )
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    YEARS_ACTIVE_CHOICES = (
        ('0-1', '0-1'),
        ('1-2', '1-2'),
        ('2-4', '2-4'),
        ('4-above', '4-above'),
    )

    CONTRACT_CHOICES = (
        ('fulltime', 'fulltime'),
        ('contract', 'contract'),
        ('remote', 'remote'),
        ('freelance', 'freelance'),

    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, null=True, blank=True, max_length=30)
    stage = models.CharField(choices=STAGE_CHOICES, default='profile_type_selection', max_length=100)
    profile_photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    csa = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=30)
    phone_number = models.CharField(null=True, max_length=30)
    # developer profile
    linkedin_url = models.CharField(max_length=500, null=True, )
    portfolio = models.CharField(max_length=500, blank=True, null=True)
    github_repo = models.CharField(max_length=500, null=True, )
    language = models.CharField(max_length=140, null=True, blank=True)
    framework = models.CharField(max_length=140, null=True, blank=True)
    years = models.CharField(choices=YEARS_ACTIVE_CHOICES, null=True, max_length=30)
    about = models.CharField(null=True, max_length=300)
    profile_tags = SeparatedValuesField(null=True, max_length=150, token=',')
    skills = models.CharField(max_length=900, null=True, blank=True)
    verified_skills = models.CharField(max_length=900, null=True, blank=True)
    country = CountryField(null=True, max_length=30)
    availabilty = models.CharField(choices=CONTRACT_CHOICES, null=True, max_length=30)

    # years = models.CharField(max_length=30, choices=YEARS_ACTIVE_CHOICES, null=True, blank=True),

    # recruiter profile
    company = models.CharField(max_length=140, null=True, blank=True)
    job_role = models.CharField(max_length=140, null=True, blank=True)
    industry = models.CharField(max_length=80, null=True, blank=True)
    company_url = models.CharField(max_length=500, null=True, blank=True)
    tags = TaggableManager()
    file = CloudinaryField(resource_type="raw", blank=True)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False

    def photo(self, default_path="default_user_photo.png"):
        if self.profile_photo:
            return self.profile_photo
        return default_path

    def get_absolute_url(self):
        return '/accounts/profile/'

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def date_joined(self):
        return self.user.date_joined

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
