from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        print("GET request to logout")
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("POST request to logout")
        return super().post(request, *args, **kwargs)

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            send_mail(
                'Обояшки рады Вам!',
                'Спасибо за регистрацию у нас!',
                'bobrysheva_oxana@mail.ru',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Вы зарегистрировались у нас на сайте успешно, теперь можете авторизоваться!')
            return redirect('users:login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


