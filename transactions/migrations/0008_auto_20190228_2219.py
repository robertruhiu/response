# Generated by Django 2.1.5 on 2019-02-28 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20190228_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opencall',
            name='projecttitle',
        ),
        migrations.AddField(
            model_name='transaction',
            name='projecttitle',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
