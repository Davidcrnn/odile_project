from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput

# from allauth.account.forms import SignupForm

LIVRAISON_CHOICES = (
    ('1', 'Point fixe 1'),
    ('2', 'Point fixe - Loueur de bateau'),
    ('3', 'Livraison sur bateau')
)

OBJET_CHOICES = (
    ('livraison', 'Livraison'),
    ('qualité du service', 'Qualité du service'),
    ('produits', 'Produits'),
    ('autre', 'Autre'),
)


class CheckoutForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input'
    }))
    prenom = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Alan',
        'class': 'form-control checkout-input'
    }))
    phone = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={
        'placeholder': '0145444646',
        'class': 'form-control checkout-input'
    }))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Alan@turing.com',
        'class': 'form-control checkout-input'
    }))

    code_postal = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={
        'placeholder': '75000',
        'class': 'form-control checkout-input',

    }))
    pays = CountryField(blank_label='(Pays)').formfield(

        required=False, widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100 checkout-input',
        }))
    delivery_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=LIVRAISON_CHOICES)

    date_delivery = forms.CharField(max_length=100, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "my-custom-class",
            "placeholder": 'Choisir une date de livraison',
        },
        options={  # flatpickr options
            "dateFormat": "d/m/Y H:i",
            'minTime': '10:00',
            'maxTime': '12:30',
            'enableTime': 'true',
            'time_24hr': 'true',
            'minDate': "today",
            'minuteIncrement': '10',
            "locale": "fr",
        }
    ))

    address_default = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
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

# class CustomSignupForm(SignupForm):
#     username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
#         'placeholder': 'Alan@turing.com',
#         'class': 'form-control checkout-input'
#     }))
#     email = forms.CharField(widget=forms.TextInput(attrs={

#         'placeholder': 'Alan@turing.com',
#         'class': 'form-control checkout-input'
#     }))

#     password1 = forms.CharField(widget=forms.TextInput(attrs={
#         'placeholder': 'Identifiant',
#         'class': 'form-control checkout-input'
#     }))

#     password2 = forms.CharField(widget=forms.PasswordInput)


# class AvisForm(forms.Form):

#     email = forms.EmailField(widget=forms.TextInput(attrs={
#         'placeholder': 'Alan@turing.com',
#         'class': 'form-control '
#     }))
#     objet = forms.ChoiceField(choices=OBJET_CHOICES,
#                               widget=forms.RadioSelect(attrs={
#                                   'class': 'inline-check radio-display'
#                               }))
#     message = forms.CharField(widget=forms.Textarea(attrs={
#         'placeholder': '75000',
#         'class': 'form-control '}))
