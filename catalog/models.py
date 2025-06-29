from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name="Наименование")
    product_description = models.TextField()
    product_image = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена покупки"
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания продукта"
    )
    updated_at = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения продукта"
    )

    def __str__(self):
        return f"{self.product_name} вы можете приобрести сегодня за {self.purchase_price} рублей."

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category__category_name", "product_name"]


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Категория")
    category_description = models.TextField(
        verbose_name="Описание категории", blank=True, null=True
    )

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["category_name"]
