# Generated by Django 3.1 on 2021-01-07 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0010_studentchoice_classtestsolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentchoice',
            name='classtestsolution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearn.classtestsolution'),
        ),
    ]
