# Generated by Django 2.2.10 on 2022-03-04 09:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20220302_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
