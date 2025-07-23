from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Delete products and categories before loading test " "data from fixture"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "products_fixture.json", "categories_fixture.json")
        self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры"))
