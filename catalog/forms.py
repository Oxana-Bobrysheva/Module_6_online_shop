import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


forbidden_words = ["казино","криптовалюта",
"крипта","биржа","дешево","бесплатно","обман",
"полиция","радар"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_name",
            "product_description",
            "product_image",
            "category",
            "purchase_price",
        ]
        exclude = ["created_at", "updated_at"]
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Введите название продукта'})
        self.fields['product_description'].widget.attrs.update({'class': 'form-control',
                                                        'placeholder': 'Введите описание продукта'})
        self.fields['product_image'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['purchase_price'].widget.attrs.update({'class': 'form-control',
                                                        'placeholder': 'Введите цену', 'type': 'float'})

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        product_description = cleaned_data.get('product_description')

        for word in forbidden_words:
            pattern = rf'\b{re.escape(word)}\b'
            if re.search(pattern, product_name, re.IGNORECASE):
                self.add_error('product_name',
                               f'Внимание! Слово "{word}" не может быть использовано в названии продукта!')
                break
        for word in forbidden_words:
            pattern = rf'\b{re.escape(word)}\b'
            if re.search(pattern, product_description, re.IGNORECASE):
                self.add_error('product_description',
                               f'Внимание! Слово "{word}" не может быть использовано в описании продукта!')
                break

        return cleaned_data

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')

        if price <= 0:
            raise ValidationError("Цена продукта не может быть отрицательной или равной нулю!")
        return price