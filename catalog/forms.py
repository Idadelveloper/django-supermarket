from  django import forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from pkg_resources import require

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class AddressForm(forms.Form):
    street_address = forms.CharField(required=False)
    apartment_address = forms.CharField(required=False)
    country = CountryField(blank_label="Select country").formfield(widget=CountrySelectWidget(attrs={
        "class":"custom-select d-block w-100"
    }), required=False)
    zip = forms.CharField(required=False)
    save_info = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)