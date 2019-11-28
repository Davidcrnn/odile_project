from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

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

    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,

            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
