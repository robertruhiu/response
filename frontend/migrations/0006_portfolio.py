# Generated by Django 2.1.5 on 2019-02-25 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0005_submissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, null=True)),
                ('description', models.CharField(max_length=400, null=True)),
                ('image', models.CharField(max_length=400, null=True)),
                ('repository_link', models.CharField(max_length=400, null=True)),
                ('demo_link', models.CharField(max_length=400, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
