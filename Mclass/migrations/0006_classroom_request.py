# Generated by Django 3.2.13 on 2023-10-08 09:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mclass', '0005_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='request',
            field=models.ManyToManyField(related_name='request', to=settings.AUTH_USER_MODEL),
        ),
    ]