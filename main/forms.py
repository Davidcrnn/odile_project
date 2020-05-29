from allauth.account.forms import SignupForm
from django import forms
from django.forms import ModelForm
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.utils.timezone import datetime
from .models import Avis
from django.conf import settings


LIVRAISON_CHOICES = (
    ('ecole-de-voile', 'Ecole de voile'),
    ('loueur-bateau', 'Loueur bateau'),
    ('bateau-fixe', 'Bateau fixe'),
    ('livraison-sur-bateau', 'Livraison sur bateau'),
)

LOUEUR_CHOICES = (
    ('', 'Choisissez'),
    ('bat-express', 'Bat Express'),
    ('ferret-marine', 'Ferret Marine'),
    ('sensey', 'Sensey')
)

OBJET_CHOICES = (
    ('livraison', 'Livraison'),
    ('qualité du service', 'Qualité du service'),
    ('produits', 'Produits'),
    ('autre', 'Autre'),
)

ZONE_LIVRAISON_BATEAU = (
    ('-- Choisissez une zone --',
     (
         ('', 'Choisissez'),
         ('4', 'Zone 4'),
         ('5a', 'Zone 5a'),
         ('5b', 'Zone 5b'),
         ('6', 'Zone 6'),
         ('7', 'Zone 7'),

     )
     ),
)
CRENEAU_DELIVERY = (
    ('-- Zone 4 et Zone 5b --',
        (
            ('', 'Choisissez'),
            ('10:30', '10:30'),
            ('10:40', '10:40'),
            ('10:50', '10:50'),
            ('11:30', '11:30'),
            ('11:40', '11:40'),
            ('11:50', '11:50'),
        )
     ),

    ('-- Zone 5a Zone 6 et 7 --',
        (
            ('10:00', '10:00'),
            ('10:10', '10:10'),
            ('10:20', '10:20'),
            ('11:00', '11:00'),
            ('11:10', '11:10'),
            ('11:20', '11:20'),
        )
     ),
)

COUVERT_CHOICES = (
    ('-- Nombre de couverts --',
        (
            ('', 'Choisissez'),
            ('Pas besoin', 'Pas besoin'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),

        )
     ),

)


class CheckoutForm(forms.Form):

    couvert = forms.ChoiceField(
        required=True, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'data-size': "5"
            }
        ), choices=COUVERT_CHOICES)

    name = forms.CharField(required=True, label='Nom', error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))

    prenom = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'form-control checkout-input',
        }))

    phone = forms.CharField(max_length=13, label='Téléphone', help_text='Numéro valide', error_messages={
        'required': "Vous devez renseigner ce champ"}, required=True, widget=forms.TextInput(attrs={
            'placeholder': '0145444646',
            'class': 'form-control checkout-input',
        }))
    email = forms.EmailField(required=True, help_text='Rentrez votre email', error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan@turing.com',
            'class': 'form-control checkout-input',
        }))

    delivery_option = forms.ChoiceField(required=True,
                                        widget=forms.RadioSelect,
                                        choices=LIVRAISON_CHOICES,
                                        help_text='Choississez une date de livraison et son horaire')

    date_de_livraison = forms.CharField(required=True, help_text="Les commandes pour le déjeuner doivent être prises au plus tard la veille pour le lendemain ", error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "checkout-input",
            "placeholder": 'Choisir une date de livraison',
            "id": 'datepicker-dejeuner',

        }
    ))

    save_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    zone_delivery = forms.ChoiceField(
        label='Zone de livraison', required=False, widget=forms.Select(attrs={'class': 'selectpicker'}), choices=ZONE_LIVRAISON_BATEAU)

    rang_delivery = forms.CharField(label='Rang', required=False, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))
    numero_delivery = forms.CharField(label='Numéro', required=False, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))

    creneau_delivery = forms.ChoiceField(
        required=False,
        label='Heure de livraison',
        widget=forms.Select(attrs={
            'id': 'select-time',
            'class': 'selectpicker',
            'data-size': "5",
            'data-hide-disabled': 'true',
        }), choices=CRENEAU_DELIVERY)

    loueur_bateau = forms.ChoiceField(
        label='Préciser le loueur de bateau', required=False, widget=forms.Select(attrs={'class': 'selectpicker'}), choices=LOUEUR_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        delivery_option = cleaned_data.get('delivery_option')
        loueur_bateau = cleaned_data.get('loueur_bateau')
        zone_delivery = cleaned_data.get('zone_delivery')
        creneau_delivery = cleaned_data.get('creneau_delivery')
        rang_delivery = cleaned_data.get('rang_delivery')
        numero_delivery = cleaned_data.get('numero_delivery')

        list = ['10:30', '10:40', '10:50', '11:30', '11:40', '11:50']
        list1 = ['10:00', '10:10', '10:20', '11:00', '11:10', '11:20']

        if delivery_option == "livraison-sur-bateau" and (rang_delivery == "" or numero_delivery == ""):
            msg = 'Vous devez préciser votre emplacement'
            if rang_delivery == "":
                self.add_error('rang_delivery', msg)
                self.add_error('delivery_option', msg)
            elif numero_delivery == "":
                self.add_error('numero_delivery', msg)
                self.add_error('delivery_option', msg)
            else:
                self.add_error('delivery_option', msg)

        if (zone_delivery == '4' or zone_delivery == '5b') and creneau_delivery not in list:
            msg = 'Vous devez sélectionner un créneau horaire correspondant à votre zone'
            self.add_error('delivery_option', msg)
            self.add_error('creneau_delivery', msg)

        if (zone_delivery == '5a' or zone_delivery == '6' or zone_delivery == '7') and creneau_delivery not in list1:
            msg = 'Vous devez sélectionner un créneau horaire correspondant à votre zone'
            self.add_error('delivery_option', msg)
            self.add_error('creneau_delivery', msg)

        if delivery_option == 'loueur-bateau' and loueur_bateau == '':
            msg = 'Vous devez préciser un loueur de bateau'
            self.add_error('delivery_option', msg)
            self.add_error('loueur_bateau', msg)


class CheckoutAperoForm(forms.Form):

    couvert = forms.ChoiceField(
        required=True, widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'data-size': "5"
            }
        ), choices=COUVERT_CHOICES)

    name = forms.CharField(required=True, label='Nom', error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))
    prenom = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'form-control checkout-input',
        }))
    phone = forms.CharField(max_length=13, label='Téléphone', error_messages={
        'required': "Vous devez renseigner ce champ"}, required=True, widget=forms.TextInput(attrs={
            'placeholder': '0145444646',
            'class': 'form-control checkout-input',
        }))
    email = forms.EmailField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan@turing.com',
            'class': 'form-control checkout-input',
        }))

    date_de_livraison = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "checkout-input form-control",
            "placeholder": 'Choisir une date de livraison',
            "id": 'datepicker-apero',
        }
    ))

    save_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    # cgv = forms.BooleanField(required=True)


class ProductForm(forms.Form):

    QUANTITY_PRODUCT = (
        ('-- Choisissez une quantité --',
         (
             ('1', 1),
             ('2', 2),
             ('3', 3),
             ('4', 4),
             ('5', 5),
             ('6', 6),
             ('7', 7),
             ('8', 8),
             ('9', 9),
             ('10', 10),
         )
         ),
    )

    VAR_CATEGORIES = (
        ('boisson', 'boisson'),
        ('sandwich', 'sandwich'),
        ('dessert', 'dessert'),
        ('huitre', 'huitre'),
        ('alcool', 'alcool')
    )

    quantity = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "selectpicker",
        }), choices=QUANTITY_PRODUCT, label='Choisissez la quantité:', initial='--Choisissez une quantité --')

    sandwich = forms.CharField(required=False,
                               widget=forms.RadioSelect, label='Choisissez votre sandwich :')
    boisson = forms.CharField(required=False,
                              widget=forms.RadioSelect, label='Choisissez votre boisson :')
    dessert = forms.CharField(required=False,
                              widget=forms.RadioSelect, label='Choisissez votre dessert :')
    alcool = forms.CharField(required=False,
                             widget=forms.RadioSelect, label='Choisissez une option :')
    huitre = forms.CharField(required=False,
                             widget=forms.RadioSelect, label='Choisissez une option :')


class DeliveredForm(forms.Form):
    is_delivered = forms.BooleanField(
        required=True, widget=forms.CheckboxInput())


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Promo code',
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField(label="Référence de la commande", widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Votre référence commande ...'
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Votre email ...'
    }))
    message = forms.CharField(label="Motifs de votre demande", widget=forms.Textarea(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Votre message ...'

    }))

    def __str__(self):
        return f"{self.pk}"


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class AvisForm(forms.Form):

    OBJET = (
        ('Produits', 'Produits'),
        ('Livraison', 'Livraison'),
        ('Horaires de livraison', 'Horaires de livraison'),
        ('Autre', 'Autre'),
    )

    objet = forms.ChoiceField(required=True,
                              widget=forms.RadioSelect,
                              choices=OBJET,
                              )
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Votre email ...',
        'class': 'form-control checkout-input'}))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Votre message nous permettra d'améliorer nos services ...",
        'class': 'form-control checkout-input',
        'rows': 10,
    }))


class ContactForm(forms.Form):
    from_email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Votre email ...',
        'class': 'form-control checkout-input'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Une petite question ...",
        'class': 'form-control checkout-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 10,
        'placeholder': 'Votre message ...',
        'class': 'form-control checkout-input '}))


class CustomSignupForm(SignupForm):
    prenom = forms.CharField(
        max_length=30, label='Prenom', widget=forms.TextInput
        (attrs={'placeholder': 'Prenom'}))
    name = forms.CharField(max_length=30, label='Nom', widget=forms.TextInput
                           (attrs={'placeholder': 'Nom'}))

    def signup(self, request, user):
        user.prenom = self.cleaned_data['prenom']
        user.name = self.cleaned_data['name']
        user.save()
        return user
