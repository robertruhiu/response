# Generated by Django 2.0.4 on 2018-11-20 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20181120_1518'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='framework',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='projects.Framework'),
            preserve_default=False,
        ),
    ]
