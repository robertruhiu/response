# Generated by Django 2.0.4 on 2018-12-14 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_auto_20181214_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id',
            field=models.BigIntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]