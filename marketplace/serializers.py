from django.contrib.auth.models import User
from marketplace.models import DevRequest,Job,JobApplication
from rest_framework import serializers



class DevRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = DevRequest
        fields = '__all__'

class JobRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'

class JobApplicationsRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = '__all__'

