from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from .models import Newsletter
# from allauth.account.forms import SignupForm

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)


class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Turing',
        'class': 'form-control checkout-input'
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Alan',
        'class': 'form-control checkout-input'
    }))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'placeholder': '0145444646',
        'class': 'form-control checkout-input'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Alan@turing.com',
        'class': 'form-control checkout-input'
    }))
    adresse = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '12 rue de sèvres',
        'class': 'form-control checkout-input'
    }))
    code_postal = forms.CharField(max_length=13, widget=forms.TextInput(attrs={
        'placeholder': '75000',
        'class': 'form-control checkout-input'
    }))
    pays = CountryField(blank_label='(Pays)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100 checkout-input',
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

    def __str__(self):
        return f"{self.pk}"


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

class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ['email']
