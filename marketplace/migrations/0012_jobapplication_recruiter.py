# Generated by Django 2.2 on 2019-07-24 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0011_auto_20190723_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='recruiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobrecruiter', to=settings.AUTH_USER_MODEL),
        ),
    ]