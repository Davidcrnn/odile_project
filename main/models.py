from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
