# Generated by Django 2.2 on 2020-05-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0052_auto_20200514_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='bouchon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
