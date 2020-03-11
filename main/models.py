from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
import datetime
from django.utils.timezone import now


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

LIVRAISON_CHOICES = (
    ('1', 'Point fixe 1'),
    ('2', 'Point fixe - Loueur de bateau'),
    ('3', 'Livraison-sur-bateau')
)

MENU = (
    ('Apero', 'Apero'),
    ('Dejeuner', 'Dejeuner')
)

TYPE_OF_ORDER = (
    ('Dejeuner', 'Dejeuner'),
    ('Apero', 'Apero')
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(verbose_name='Prix')
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField()
    category = models.CharField(
        max_length=32, choices=PRODUCT_CATEGORIES, default='Plats')
    allergene = models.CharField(
        max_length=32, choices=PRODUCT_ALLERGENES, blank=True, null=True)
    menu = models.CharField(max_length=30, choices=MENU, default='Dejeuner')
    quantite = models.IntegerField(default=1)

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
    date_delivery = models.CharField(max_length=100)
    # date_publication = models.DateField(auto_now_add=False, blank=True, null=True)
    delivery_option = models.CharField(
        max_length=100, choices=LIVRAISON_CHOICES)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    cgv = models.BooleanField(default=False)
    type_of_order = models.CharField(
        max_length=50, choices=TYPE_OF_ORDER, default='Dejeuner')
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    date_de_creation = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_quantity(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.quantity
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
        return self.user.email

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
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    code_postal = models.IntegerField()
    pays = CountryField(multiple=False)
    default = models.BooleanField(default=False)
    zone_delivery = models.CharField(max_length=30)
    rang_delivery = models.CharField(max_length=20)
    numero_delivery = models.CharField(max_length=30)

    def __str__(self):
        return self.user.email


class Avis(models.Model):

    OBJET = (
        ('Produits', 'Produits'),
        ('Livraison', 'Livraisons'),
        ('Horaires de livraison', 'Horaires de livraison'),
        ('Autre', 'Autre'),
    )

    email = models.EmailField()
    objet = models.CharField(max_length=50, choices=OBJET)
    message = models.TextField()

    def __str__(self):
        return self.objet
