# Generated by Django 2.2 on 2020-06-04 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_auto_20200529_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.FloatField(default=0, verbose_name='Prix'),
        ),
    ]
