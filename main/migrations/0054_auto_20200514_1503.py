# Generated by Django 2.2 on 2020-05-14 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_orderproduct_bouchon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='bouchon',
            new_name='alcool',
        ),
    ]
