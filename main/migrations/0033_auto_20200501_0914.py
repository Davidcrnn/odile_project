# Generated by Django 2.2 on 2020-05-01 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20200501_0846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='code_postal',
        ),
        migrations.RemoveField(
            model_name='info',
            name='pays',
        ),
    ]
