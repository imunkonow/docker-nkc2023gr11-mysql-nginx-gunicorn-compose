# Generated by Django 4.1.2 on 2022-10-28 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
    ]
