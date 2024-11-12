import secrets
import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from newsletter.forms import StyleFormMixin
from users.forms import UserAuthenticationForm, UserRegisterForm, UserForm, ResetPasswordForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = UserAuthenticationForm


class LogoutView(BaseLogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Верификация почты"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение верификации"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_object(self, queryset=None):
        return self.request.user


class UserResetPasswordView(PasswordResetView, StyleFormMixin):
    """
    Сброс пароля с использованием email
    """
    form_class = ResetPasswordForm
    template_name = 'users/forgot_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Проверяет валидность и сохраняет новый пароль
        """
        email = form.cleaned_data['email']
        # Проверяем наличие пользователя с указанной почтой
        try:
            user = User.objects.get(email=email)
            if user:
                # Создаем новый пароль для пользователя и отправляем его на почту
                password = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(0, 10)])
                user.set_password(password)
                user.is_active = True
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f'Новый пароль: {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
            return redirect(reverse('users:login'))
        except User.DoesNotExist:
            # Если пользователь не найден, перенаправляем на страницу регистрации
            return redirect(reverse('users:register'))


def generate_new_password(request):
    """Генерирование нового пароля с отправкой на почту"""
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Смена пароля',
        message=f'Пароль заменен на: {new_password}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect('users:login')


class UserListView(ListView):
    model = User


def block_user(request, pk):
    """Заблокировать пользователя"""
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.is_staff = False
    user.is_superuser = False
    user.save()
    return redirect('users:list')
