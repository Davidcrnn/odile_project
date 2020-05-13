# Generated by Django 2.2 on 2020-05-04 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_remove_orderproduct_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ManyToManyField(to='main.Product'),
        ),
    ]
