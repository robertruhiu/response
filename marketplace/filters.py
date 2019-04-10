from django.contrib.auth.models import User
import django_filters


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'profile__language',
            'profile__framework',
            'profile__years',
            'profile__country',
            'profile__availabilty',
        ]
