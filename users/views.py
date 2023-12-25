import random

from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View, UpdateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:code')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_pass = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        new_user = form.save(commit=False)
        new_user.code = new_pass
        new_user.save()
        send_mail(
            recipient_list=[new_user.email],
            message=f'Для подтверждения email введите код {new_user.code}',
            subject='Регистрация на сервисе',
            from_email=DEFAULT_FROM_EMAIL,
        )

        client_group = Group.objects.get(name='Клиент')
        client_group.user_set.add(new_user)

        return super().form_valid(form)


class CodeView(View):
    model = User
    template_name = 'users/code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print(type(request))
        code = request.POST.get('code')
        user = User.objects.filter(code=code).first()

        if user is not None and user.code == code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_pass = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    request.user.set_password(new_pass)
    request.user.save()
    send_mail(
        subject='Изменение пароля',
        message=f'Ваш пароль изменен на {new_pass}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
    )
    return redirect(reverse('users:login'))


