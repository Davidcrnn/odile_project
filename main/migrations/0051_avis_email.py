# Generated by Django 2.2 on 2020-05-14 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_auto_20200504_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='avis',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
