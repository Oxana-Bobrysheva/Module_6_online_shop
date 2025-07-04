from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


def home(request):
    product_list = Product.objects.all().order_by("id")
    paginator = Paginator(product_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,}

    return render(request, "catalog/home.html", context)


def contacts(request):
    success = False
    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")
        print(f"Новое сообщение от {name}, телефон: {phone}. Текст: {message}")
        success = True
    return render(request, "catalog/contacts.html", {"success": success})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')  # замените на нужный URL
    else:
        form = ProductForm()
    return render(request, 'catalog/product_create.html', {'form': form})