# Generated by Django 2.0.4 on 2019-01-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='years',
            field=models.CharField(choices=[('0-1', '0-1'), ('1-2', '1-2'), ('2-4', '2-4'), ('4-above', '4-above')], max_length=30, null=True),
        ),
    ]
