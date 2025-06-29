from django.shortcuts import render


def home(request):
    return render(request, "catalog/home.html")

def contacts(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'Новое сообщение от {name}, телефон: {phone}. Текст: {message}')
        success = True
    return render(request, 'catalog/contacts.html', {'success': success})