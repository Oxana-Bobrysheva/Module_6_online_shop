import re

from django import forms
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
