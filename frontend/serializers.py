from django.contrib.auth.models import User
from accounts.models import Profile
from frontend.models import Experience,Portfolio
from rest_framework import serializers
from django_countries import Countries

class SerializableCountryField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(SerializableCountryField, self).__init__(choices=Countries())

    def to_representation(self, value):
        if value in ('', None):
            return '' # normally here it would return value. which is Country(u'') and not serialiable
        return super(SerializableCountryField, self).to_representation(value)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email',
                  'password','username')
class ProfileSerializer(serializers.ModelSerializer):
    country = SerializableCountryField(allow_blank=True)
    class Meta:
        model = Profile
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = '__all__'
