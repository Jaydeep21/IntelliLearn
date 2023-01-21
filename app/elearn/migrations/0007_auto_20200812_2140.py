# Generated by Django 3.0.8 on 2020-08-12 16:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('elearn', '0006_auto_20200811_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classwork',
            old_name='class_name',
            new_name='college_class',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='class_name',
            new_name='college_class',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='class_name',
            new_name='college_class',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='college_class',
            new_name='college_classes',
        ),
    ]
