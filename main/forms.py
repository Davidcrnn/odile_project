from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.utils.timezone import datetime
from .models import Avis
from django.conf import settings


LIVRAISON_CHOICES = (
    ('1', 'Point-fixe-1'),
    ('2', 'Loueur-de-bateau'),
    ('3', 'Livraison-sur-bateau')
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
        required=True, widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'data-size': "5"
            }
        ), choices=COUVERT_CHOICES)

    name = forms.CharField(required=True, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))

    prenom = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'form-control checkout-input',
        }))

    phone = forms.CharField(max_length=13, help_text='Numéro valide', error_messages={
        'required': "Vous devez renseigner ce champ"}, required=True, widget=forms.TextInput(attrs={
            'placeholder': '0145444646',
            'class': 'form-control checkout-input',
        }))
    email = forms.EmailField(required=True, help_text='Rentrez votre email', error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan@turing.com',
            'class': 'form-control checkout-input',
        }))

    code_postal = forms.CharField(max_length=13, required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': '75000',
            'class': 'form-control checkout-input',
        }))

    pays = CountryField(blank_label='Pays').formfield(
        required=True, widget=CountrySelectWidget(attrs={
            'class': 'form-control checkout-input selectpicker',
            'data-size': "5",

        }))
    delivery_option = forms.ChoiceField(required=True,
                                        widget=forms.RadioSelect,
                                        choices=LIVRAISON_CHOICES,
                                        help_text='Choississez une date de livraison et son horaire')

    # date_delivery = forms.CharField(required=True, help_text="Les commandes pour le déjeuner doivent être prises au plus tard la veille pour le lendemain ", error_messages={
    #     'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
    #     attrs={    # input element attributes
    #         "class": "checkout-input",
    #         "placeholder": 'Choisir une date de livraison',
    #         "id": 'datepicker-dejeuner',

    #     }
    # ))

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
        label='Heure de livraison',
        widget=forms.Select(attrs={
            'id': 'select-time',
            'class': 'selectpicker',
            'data-size': "5",
            'data-hide-disabled': 'true',
        }), choices=CRENEAU_DELIVERY)


class CheckoutAperoForm(forms.Form):

    couvert = forms.ChoiceField(
        required=True, widget=forms.Select(
            attrs={
                'class': 'selectpicker',
                'data-size': "5"
            }
        ), choices=COUVERT_CHOICES)

    name = forms.CharField(required=True, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))
    prenom = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'form-control checkout-input',
        }))
    phone = forms.CharField(max_length=13, error_messages={
        'required': "Vous devez renseigner ce champ"}, required=True, widget=forms.TextInput(attrs={
            'placeholder': '0145444646',
            'class': 'form-control checkout-input',
        }))
    email = forms.EmailField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan@turing.com',
            'class': 'form-control checkout-input',
        }))

    code_postal = forms.CharField(max_length=13, required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
            'placeholder': '75000',
            'class': 'form-control checkout-input',

        }))
    pays = CountryField(blank_label='(Pays)').formfield(

        required=True, widget=CountrySelectWidget(attrs={
            'class': 'form-control selectpicker',
            'data-size': "5",
            'data-live-search': "true",
        }))

    # date_delivery = forms.CharField(required=True, error_messages={
    #     'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
    #     attrs={    # input element attributes
    #         "class": "checkout-input form-control",
    #         "placeholder": 'Choisir une date de livraison',
    #         "id": 'datepicker-apero',
    #     }
    # ))

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

    quantity = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": "selectpicker",
        }), choices=QUANTITY_PRODUCT, label='Choisissez la quantité:', initial='--Choisissez une quantité --')


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

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Votre email ...'
    }))
    objet = forms.ChoiceField(required=True,
                              widget=forms.RadioSelect,
                              choices=OBJET,
                              )
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Votre message nous permettra d'améliorer nos services ...",
        'class': 'form-control checkout-input',
        'rows': 4, 'cols': 15
    }))


class ContactForm(forms.Form):
    from_email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Votre email ...',
        'class': 'form-control checkout-input'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Une petite question ...",
        'class': 'form-control checkout-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'placeholder': 'Votre message ...',
        'class': 'form-control checkout-input '}))
