from django import forms
# from django.utils.translation import gettext_lazy as _

# Пользователь может выбрать не более 20 единиц одного товара
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # quantity = forms.IntegerField(label=_('Количество'), min_value=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
