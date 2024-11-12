from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, UserRegisterView, email_verification, UserUpdateView, \
    generate_new_password, UserResetPasswordView, block_user, UserListView

app_name = UsersConfig.name
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('genpassword/', generate_new_password, name='generate_new_password'),
    path('forgotpassword/', UserResetPasswordView.as_view(), name='forgot_password'),
    path('list/', UserListView.as_view(), name='list'),
    path('block/<int:pk>/', block_user, name='block'),
]
