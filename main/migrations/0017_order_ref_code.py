# Generated by Django 2.2 on 2019-11-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20191126_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='123', max_length=20),
            preserve_default=False,
        ),
    ]
