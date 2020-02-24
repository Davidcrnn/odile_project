# Generated by Django 2.2 on 2020-02-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_order_cgv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('objet', models.CharField(choices=[('Produits', 'Produits'), ('Livraison', 'Livraisons'), ('Horaires de livraison', 'Horaires de livraison'), ('Autre', 'Autre')], max_length=50)),
                ('message', models.TextField()),
            ],
        ),
    ]