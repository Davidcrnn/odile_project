from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.utils.timezone import datetime
from .models import Avis


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
    ('4', 'Zone 4'),
    ('5a', 'Zone 5a'),
    ('5b', 'Zone 5b'),
    ('6', 'Zone 6'),
    ('7', 'Zone 7'),
)


class CheckoutForm(forms.Form):
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
    pays = CountryField(blank_label='(Pays)').formfield(

        required=True, widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100 checkout-input',
        }))
    delivery_option = forms.ChoiceField(required=True,
                                        widget=forms.RadioSelect,
                                        choices=LIVRAISON_CHOICES,
                                        help_text='Choississez une date de livraison et son horaire')

    date_delivery = forms.CharField(help_text="Les commandes pour le déjeuner doivent être prises au plus tard la veuille pour le lendemain ", error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "checkout-input",
            "placeholder": 'Choisir une date de livraison',
            "id": 'datepicker-dejeuner',

        },
        options={  # flatpickr options
            # "dateFormat": "d/m/Y H:i",
            # "altFormat": "d/m/Y H:i",
            # 'minTime': '10:00',
            # 'maxTime': '12:30',
            # 'enableTime': 'true',
            # 'time_24hr': 'true',
            # 'minuteIncrement': '10',
            # "locale": "fr",
        }
    ))

    save_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    zone_delivery = forms.ChoiceField(
        required=False, widget=forms.Select(attrs={
            'placeholder': 'Rang du bateau',
            'class': 'form-control checkout-input',
        }), choices=ZONE_LIVRAISON_BATEAU,)

    rang_delivery = forms.CharField(required=False, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Rang du bateau',
        'class': 'form-control checkout-input',
    }))
    numero_delivery = forms.CharField(required=False, error_messages={'required': "Vous devez renseigner ce champ"}, widget=forms.TextInput(attrs={
        'placeholder': 'Numéro du bateau',
        'class': 'form-control checkout-input',
    }))


class CheckoutAperoForm(forms.Form):
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
            'class': 'custom-select d-block w-100 checkout-input',
        }))

    date_delivery = forms.CharField(required=True, error_messages={
        'required': "Vous devez renseigner ce champ"}, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "form-control checkout-input",
            "placeholder": 'Choisir une date de livraison',
            "id": 'datepicker-apero',
        },
        options={  # flatpickr options
            # "dateFormat": "d/m/Y H:i",
            # "altFormat": "d/m/Y H:i",
            # 'minTime': '10:00',
            # 'maxTime': '12:30',
            # 'enableTime': 'false',
            # 'time_24hr': 'true',
            # 'minDate': "today",
            # 'defaultDate': 'today',
            # 'minuteIncrement': '10',
            # "locale": "fr",
        }
    ))

    save_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())


class ProductForm(forms.Form):

    QUANTITY_PRODUCT = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
    )
    quantity = forms.ChoiceField(choices=QUANTITY_PRODUCT)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Promo code',
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __str__(self):
        return f"{self.pk}"


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CgvForm(forms.Form):
    cgv = forms.BooleanField(required=True)


class AvisForm(forms.Form):

    OBJET = (
        ('Produits', 'Produits'),
        ('Livraison', 'Livraisons'),
        ('Horaires de livraison', 'Horaires de livraison'),
        ('Autre', 'Autre'),
    )

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control checkout-input',
        'placeholder': 'Indiquez votre email'
    }))
    objet = forms.ChoiceField(required=True,
                              widget=forms.RadioSelect,
                              choices=OBJET,
                              )
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Ce message nous permettra daméliorer notre service',
        'class': 'form-control checkout-input',
        'rows': 4, 'cols': 15
    }))


class ContactForm(forms.Form):
    from_email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email@email.com',
        'class': 'form-control checkout-input'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Une petite question",
        'class': 'form-control checkout-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'placeholder': 'Votre message',
        'class': 'form-control checkout-input '}))
