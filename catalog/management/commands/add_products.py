from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **kwargs):
        category, _ = Category.objects.get_or_create(category_name='Зелень')

        products = [
            {'product_name': 'Укроп', 'product_description': 'Сорт Аллегатор', 'category': category, 'purchase_price': 65},
            {'product_name': 'Петрушка', 'product_description': 'Сорт Кудрявая', 'category': category, 'purchase_price': 70},
            {'product_name': 'Руккола', 'product_description': 'Сорт Покер', 'category': category,
             'purchase_price': 82},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно добавлен продукт: {product.product_name} по цене {product.purchase_price} рублей '
                    f'за упаковку'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Продукт уже существует: {product.product_name} по цене {product.purchase_price} рублей '
                    f'за упаковку'))