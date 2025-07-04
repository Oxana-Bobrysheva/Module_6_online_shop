from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


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
