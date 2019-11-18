from django.db import models
from django.conf import settings
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
