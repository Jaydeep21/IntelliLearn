# Generated by Django 3.1 on 2020-09-07 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0003_auto_20200907_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.college'),
        ),
    ]
