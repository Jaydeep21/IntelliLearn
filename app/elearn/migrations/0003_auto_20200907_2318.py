# Generated by Django 3.1 on 2020-09-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0002_auto_20200907_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegeclass',
            name='subjects',
        ),
        migrations.AddField(
            model_name='subject',
            name='college_class',
            field=models.ManyToManyField(blank=True, to='elearn.CollegeClass'),
        ),
    ]
