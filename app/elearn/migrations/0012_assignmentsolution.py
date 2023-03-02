# Generated by Django 3.1 on 2021-01-21 10:40

from django.db import migrations, models
import django.db.models.deletion
import elearn.models


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0011_auto_20210108_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.ImageField(upload_to=elearn.models.file_directory_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearn.classworkpost')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearn.student')),
            ],
        ),
    ]
