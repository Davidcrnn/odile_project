# Generated by Django 2.2 on 2020-05-19 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20200514_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-date_de_creation',), 'verbose_name': 'Commande', 'verbose_name_plural': 'Commandes'},
        ),
        migrations.AddField(
            model_name='product',
            name='info',
            field=models.BooleanField(default=False),
        ),
    ]
