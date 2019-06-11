# Generated by Django 2.2.2 on 2019-06-11 08:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_postcontent'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postinteraction',
            unique_together={('post', 'interaction', 'user')},
        ),
    ]