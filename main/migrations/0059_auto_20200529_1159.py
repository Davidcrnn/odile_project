# Generated by Django 2.2 on 2020-05-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_auto_20200529_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='variation',
            field=models.ManyToManyField(to='main.Variation'),
        ),
    ]
