from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
        return Article.objects.filter(is_published=True).order_by("created_at")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

