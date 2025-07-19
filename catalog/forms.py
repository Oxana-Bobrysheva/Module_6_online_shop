import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

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

    def clean_product_image(self):
        image = self.cleaned_data.get('product_image')

        if image:
            # Проверяем, что это загруженный файл (новый файл из формы)
            if isinstance(image, UploadedFile):
                # Проверяем MIME-тип файла
                valid_mime_types = ['image/jpeg', 'image/jpg', 'image/png']
                file_mime_type = image.content_type
                if file_mime_type not in valid_mime_types:
                    raise ValidationError('Поддерживаются только форматы JPEG и PNG.')

                # Проверяем размер файла
                max_size = 5 * 1024 * 1024  # 5 МБ
                if image.size > max_size:
                    raise ValidationError('Размер файла не должен превышать 5 МБ.')

        return image
