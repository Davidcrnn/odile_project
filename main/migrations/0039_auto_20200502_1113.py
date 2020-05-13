# Generated by Django 2.2 on 2020-05-02 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_productvariation_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Boisson', 'Boisson'), ('Sandwich', 'Sandwich'), ('Dessert', 'Dessert'), ('Huitre', 'Huitre')], default='Boisson', max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Prix')),
                ('visible', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Product')),
            ],
        ),
        migrations.DeleteModel(
            name='ProductVariation',
        ),
    ]
