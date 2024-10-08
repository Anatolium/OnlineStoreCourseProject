from django import forms
# from django.utils.translation import gettext_lazy as _

# Пользователь может выбрать не более 20 единиц одного товара
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Количество'))
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
