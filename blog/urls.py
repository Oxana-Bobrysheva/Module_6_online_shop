from django.urls import path
from blog.views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/", ArticleDetailView.as_view(),
         name="article_detail"),
    path("article/create/", ArticleCreateView.as_view(),
         name="article_create"),
    path(
        "article/<int:pk>/update/", ArticleUpdateView.as_view(),
        name="article_update"
    ),
    path(
        "article/<int:pk>/delete/",
        ArticleDeleteView.as_view(),
        name="article_confirm_delete",
    ),
]
