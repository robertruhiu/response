from django.contrib.auth.models import User
from projects.models import Project
from rest_framework import serializers



class Projectserializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


