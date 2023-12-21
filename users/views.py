from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            recipient_list=[new_user.email],
            message='Поздравляю, вы зарегистрировались на нашем сайте!',
            subject='Верификация',
            from_email=DEFAULT_FROM_EMAIL,
        )
        return super().form_valid(form)


