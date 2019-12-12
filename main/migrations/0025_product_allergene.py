# Generated by Django 2.2 on 2019-12-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allergene',
            field=models.CharField(blank=True, choices=[('Gluten', 'Gluten'), ('Crustaces', 'Crustaces'), ('Oeufs', 'Oeufs'), ('Poissons', 'Poissons'), ('Arachides', 'Arachides'), ('Soja', 'Entrées'), ('Lait', 'Lait'), ('Fruits a coques', 'Fruits a coques'), ('Celeri', 'Celeri'), ('Moutarde', 'Moutarde'), ('Graines de sesame', 'Graines de sesame'), ('Sulfites', 'Sulfites'), ('Lupin', 'Lupin'), ('Mollusques', 'Mollusques')], max_length=32, null=True),
        ),
    ]
