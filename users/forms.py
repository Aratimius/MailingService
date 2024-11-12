from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from newsletter.forms import StyleFormMixin
from users.models import User


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """ Форма для аутентификации"""
    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """ Форма для регистрации"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма для редактирования профиля"""
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class ResetPasswordForm(StyleFormMixin, PasswordResetForm):
    """Форма для сброса пароля"""
    class Meta:
        model = User
        fields = ('email',)
