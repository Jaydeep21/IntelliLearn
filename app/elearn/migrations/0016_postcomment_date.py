# Generated by Django 3.1 on 2021-01-21 22:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0015_auto_20210122_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
