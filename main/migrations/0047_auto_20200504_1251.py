# Generated by Django 2.2 on 2020-05-04 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_orderproduct_dessert'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='boisson',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='sandwich',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
