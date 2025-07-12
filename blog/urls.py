from django.urls import path
from blog.views import ArticleListView, ArticleDetailView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),

]