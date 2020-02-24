from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.utils.timezone import datetime


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
    name = forms.CharField(required=True, error_messages={'required': "Please Enter your Name"}, widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input',
    }))
    prenom = forms.CharField(required=True, error_messages={
        'required': "Please Enter your Name"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan',
            'class': 'form-control checkout-input',
        }))
    phone = forms.CharField(max_length=13, help_text='Numéro valide', error_messages={
        'required': "Please Enter your Name"}, required=True, widget=forms.TextInput(attrs={
            'placeholder': '0145444646',
            'class': 'form-control checkout-input',
        }))
    email = forms.EmailField(required=True, help_text='Rentrez votre email', error_messages={
        'required': "Please Enter your Name"}, widget=forms.TextInput(attrs={
            'placeholder': 'Alan@turing.com',
            'class': 'form-control checkout-input',
        }))

    code_postal = forms.CharField(max_length=13, required=True, error_messages={
        'required': "Please Enter your Name"}, widget=forms.TextInput(attrs={
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

    date_delivery = forms.CharField(required=True, error_messages={
        'required': "Please Enter your Name"}, widget=DateTimePickerInput(
        attrs={    # input element attributes
            "class": "my-custom-class",
            "placeholder": 'Choisir une date de livraison',

        },
        options={  # flatpickr options
            "dateFormat": "d/m/Y H:i",
            "altFormat": "d/m/Y H:i",
            'minTime': '10:00',
            'maxTime': '12:30',
            'enableTime': 'true',
            'time_24hr': 'true',
            'minDate': "today",
            'defaultDate': 'today',
            'minuteIncrement': '10',
            "locale": "fr",
        }
    ))

    save_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    # def clean(self):
    #     cleaned_data = super(CheckoutForm, self).clean()
    #     name = cleaned_data.get('name')
    #     email = cleaned_data.get('email')
    #     phone = cleaned_data.get('phone')
    #     prenom = cleaned_data.get('prenom')
    #     code_postal = cleaned_data.get('code_postal')
    #     pays = cleaned_data.get('pays')
    #     date_delivery = cleaned_data.get('date_delivery')
    #     today = datetime.today()

    #     if date_delivery == today.day:
    #         raise forms.ValidationError(
    #             'La livraison nest pas possible pour aujourdhui')

    #     if len(phone) > 10:
    #         raise forms.ValidationError('Ce numéro nest pas valide')

    #     if len(prenom) > 3:
    #         raise forms.ValidationError('prénom invalide')
    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if len(phone) < 10:
    #         return phone
    #     else:
    #         raise forms.ValidationError('Votre numéro nest pas correct')


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


class CgvForm(forms.Form):
    cgv = forms.BooleanField(required=True)


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
