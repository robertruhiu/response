# Generated by Django 2.1.5 on 2019-03-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_auto_20190228_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]