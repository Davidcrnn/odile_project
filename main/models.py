from django.db import models
from django.conf import settings
from django.urls import reverse
import datetime
from django.utils.timezone import now


PRODUCT_CATEGORIES = (
    ('Entrées', 'Entrées & Tapas'),
    ('Salades', 'Salades, Taboulés & Quiche'),
    ('Fromage', 'Fromages & Charcuterie'),
    ('Desserts', 'Desserts'),
    ('Enfant', 'Panier enfant'),
    ('Boissons', 'Boissons & Café'),
    ('Plats', 'Plats'),
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
LOUEUR_CHOICES = (
    ('', 'Choisissez'),
    ('bat-express', 'Bat Express'),
    ('ferret-marine', 'Ferret Marine'),
    ('sensey', 'Sensey')
)

LIVRAISON_CHOICES = (
    ('ecole-de-voile', 'Ecole de voile'),
    ('loueur-bateau', 'Loueur bateau'),
    ('bateau-fixe', 'Bateau fixe'),
    ('livraison-sur-bateau', 'Livraison sur bateau'),
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
    image = models.FileField(upload_to='images/', blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField(max_length=100)
    category = models.CharField(
        max_length=32, choices=PRODUCT_CATEGORIES, default='Plats')
    alcool = models.BooleanField(default=False)
    allergene = models.CharField(
        max_length=32, choices=PRODUCT_ALLERGENES, blank=True, null=True)
    allergene2 = models.CharField(
        max_length=32, choices=PRODUCT_ALLERGENES, blank=True, null=True)
    allergene3 = models.CharField(
        max_length=32, choices=PRODUCT_ALLERGENES, blank=True, null=True)
    menu = models.CharField(max_length=30, choices=MENU, default='Dejeuner')
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Produit'


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(visible=True)

    def boissons(self):
        return self.all().filter(category='boisson')

    def sandwichs(self):
        return self.all().filter(category='sandwich')

    def desserts(self):
        return self.all().filter(category='dessert')

    def huitres(self):
        return self.all().filter(category='huitre')


VAR_CATEGORIES = (
    ('boisson', 'boisson'),
    ('sandwich', 'sandwich'),
    ('dessert', 'dessert'),
    ('huitre', 'huitre'),
)


class Variation(models.Model):
    product = models.ManyToManyField(Product)
    category = models.CharField(
        max_length=100, choices=VAR_CATEGORIES, default='boisson')
    title = models.CharField(max_length=100)
    price = models.FloatField(verbose_name='Prix', null=True, blank=True)
    visible = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    dessert = models.CharField(max_length=100, null=True, blank=True)
    boisson = models.CharField(max_length=100, null=True, blank=True)
    sandwich = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'Commande - Produit'
        verbose_name_plural = 'Commande - Produits'


class Order(models.Model):
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    type_of_order = models.CharField(
        max_length=50, choices=TYPE_OF_ORDER, default='Dejeuner')
    products = models.ManyToManyField(OrderProduct)
    ref_code = models.CharField(max_length=20)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    information = models.ForeignKey(
        'Info', on_delete=models.SET_NULL, blank=True, null=True)
    date_de_creation = models.DateTimeField(default=now)
    date_delivery = models.CharField(max_length=100)
    date_de_livraison = models.DateTimeField(
        default=now, blank=True)
    creneau_delivery = models.CharField(
        max_length=30, default='10', blank=True, null=True)
    # date_publication = models.DateField(auto_now_add=False, blank=True, null=True)
    delivery_option = models.CharField(
        max_length=100, choices=LIVRAISON_CHOICES)
    loueur_bateau = models.CharField(
        max_length=100, choices=LOUEUR_CHOICES, blank=True, null=True)
    couvert = models.CharField(max_length=32, default='1')
    # cgv = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

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

    def get_is_delivered_url(self):
        return reverse('is_delivered', kwargs={'ref_code': self.ref_code})

    # def get_GeneratePdf_url(self):
    #     return reverse('GeneratePdf', kwargs={'ref_code': self.ref_code})


class Meta:
    ordering = ('-date_de_creation',)
    verbose_name = 'Commande'
    verbose_name_plural = 'Commandes'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Paiement'


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

    class Meta:
        verbose_name = 'Demande de remboursement'
        verbose_name_plural = 'Demandes de remboursement'


class Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    default = models.BooleanField(default=False)
    zone_delivery = models.CharField(max_length=30, blank=True, null=True)
    rang_delivery = models.CharField(max_length=20, blank=True, null=True)
    numero_delivery = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Informations utilisateurs'
        verbose_name_plural = 'Informations utilisateurs'


class Avis(models.Model):

    OBJET = (
        ('Produits', 'Produits'),
        ('Livraison', 'Livraisons'),
        ('Horaires de livraison', 'Horaires de livraison'),
        ('Autre', 'Autre'),
    )

    objet = models.CharField(max_length=50, choices=OBJET)
    message = models.TextField()

    def __str__(self):
        return self.objet

    class Meta:
        verbose_name = 'Recommandation utilisateur'
        verbose_name_plural = 'Recommadation utilisateur'
