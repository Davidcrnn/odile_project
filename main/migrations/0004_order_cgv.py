# Generated by Django 2.2 on 2020-02-24 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_order_date_de_creation'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cgv',
            field=models.BooleanField(default=False),
        ),
    ]
