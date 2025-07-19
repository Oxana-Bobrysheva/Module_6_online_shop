from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from blog.models import Article


# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        """Function that returns published articles,
        in order: newest first"""
        return Article.objects.filter(
            is_published=True).order_by("-created_at")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = (
            obj.views_count + 1
        )  # увеличиваем счётчик просмотров
        obj.save(update_fields=["views_count"])
        return obj


class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "text", "image", "is_published"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["title", "text", "image", "is_published"]
    template_name = "blog/article_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:article_detail",
                            kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")
