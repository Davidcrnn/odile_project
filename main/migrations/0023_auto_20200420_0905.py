# Generated by Django 2.2 on 2020-04-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20200417_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='numero_delivery',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='rang_delivery',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='zone_delivery',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]