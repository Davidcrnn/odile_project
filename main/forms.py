from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)


class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control'
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Alan',
        'class': 'form-control'
    }))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'placeholder': '0145444646',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Alan@turing.com',
        'class': 'form-control'
    }))
    adresse = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '12 rue de sèvres',
        'class': 'form-control'
    }))
    code_postal = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'placeholder': '75000',
        'class': 'form-control'
    }))
    pays = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class DeliveryForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
