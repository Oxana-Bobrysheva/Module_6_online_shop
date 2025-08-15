from .models import Product

def get_products_by_category(category):
    """
    Возвращает список всех продуктов в указанной категории.
    """
    return Product.objects.filter(category=category)
