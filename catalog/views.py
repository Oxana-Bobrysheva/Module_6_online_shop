from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import ProductForm, ProductModeratorForm
from .models import Product, Category
from .services import get_products_by_category
from django.shortcuts import render, get_object_or_404


def home(request):
    categories = Category.objects.all()  # Извлекаем все категории
    selected_category_id = request.GET.get('category', '')  # Получаем выбранную категорию из GET-запроса

    # Если выбрана категория, фильтруем продукты по ней
    if selected_category_id:
        products = Product.objects.filter(category_id=selected_category_id)
    else:
        products = Product.objects.all()  # Или все продукты, если категория не выбрана

    context = {
        'categories': categories,
        'products': products,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "model"
    paginate_by = 6
    ordering = ["id"]


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")
        print(f"Новое сообщение от {name}, телефон: {phone}. Текст: {message}")
        return self.render_to_response(self.get_context_data(success=True))

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        is_moderator = self.request.user.groups.filter(name='Moderators of products').exists()
        context['is_moderator'] = is_moderator
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    permission_required = 'catalog.add_product'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied

    def form_valid(self, form):
        # Сначала вызываем метод родительского класса для сохранения формы
        response = super().form_valid(form)

        # Очистка кэша для страницы продукта
        cache_key = f'product_detail_{self.object.pk}'
        cache.delete(cache_key)

        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()
        if product.owner == self.request.user:
            return True
        return self.request.user.groups.filter(name="Moderators of products").exists()


class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_list_by_category.html'
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return get_products_by_category(category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        print(f"Category ID: {category_id}")  # Логируем category_id
        context['categories'] = Category.objects.all()  # Получаем все категории
        context['category'] = get_object_or_404(Category, id=category_id)
        return context