from django import forms
from .models import Order, Review, RATE_CHOICES
from .bulma_mixin import BulmaMixin


class OrderForm(BulmaMixin, forms.ModelForm):
    address = forms.CharField(label='Write your address')
    phone = forms.CharField(label='Write your phone')

    class Meta:
        model = Order
        fields = ['phone', 'address']


class RateForm(forms.ModelForm, BulmaMixin):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), label='Leave your review here')
    rate = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Rate product from one to five')

    class Meta:
        model = Review
        fields = ['text', 'rate']
