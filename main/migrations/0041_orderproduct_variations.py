# Generated by Django 2.2 on 2020-05-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20200502_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(to='main.Variation'),
        ),
    ]