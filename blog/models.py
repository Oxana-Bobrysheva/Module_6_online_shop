from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Содержимое статьи")
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания статьи"
    )
    is_published = models.BooleanField(verbose_name="Опубликовано",
                                       default=False)
    views_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров", default=0
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
