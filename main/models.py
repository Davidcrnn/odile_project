from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField


PRODUCT_CATEGORIES = (
    ('Entrées', 'Entrées'),
    ('Boissons', 'Boissons'),
    ('Plats', 'Plats'),
    ('Desserts', 'Desserts'),
    ('Accessoires', 'Accessoires'),
)

PRODUCT_ALLERGENES = (
    ('Gluten', 'Gluten'),
    ('Crustaces', 'Crustaces'),
    ('Oeufs', 'Oeufs'),
    ('Poissons', 'Poissons'),
    ('Arachides', 'Arachides'),
    ('Soja', 'Entrées'),
    ('Lait', 'Lait'),
    ('Fruits a coques', 'Fruits a coques'),
    ('Celeri', 'Celeri'),
    ('Moutarde', 'Moutarde'),
    ('Graines de sesame', 'Graines de sesame'),
    ('Sulfites', 'Sulfites'),
    ('Lupin', 'Lupin'),
    ('Mollusques', 'Mollusques'),

)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(verbose_name='Prix')
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField()
    category = models.CharField(
        max_length=32, choices=PRODUCT_CATEGORIES, default='Plats')
    allergene = models.CharField(
        max_length=32, choices=PRODUCT_ALLERGENES, blank=True, null=True)

    quantité = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})

    # class Meta:
    #     verbose_name = 'Produit'


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    # class Meta:
    #     verbose_name = 'Commande - Produit'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ref_code = models.CharField(max_length=20)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    information = models.ForeignKey(
        'Info', on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    # class Meta:
    #     verbose_name = 'Commande'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    # class Meta:
    #     verbose_name = 'Paiement'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField()
    adresse = models.CharField(max_length=60)
    code_postal = models.IntegerField()
    pays = CountryField(multiple=False)
    # TODO
    # datetime_field

    def __str__(self):
        return self.user.username
