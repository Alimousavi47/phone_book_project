from django.urls import path
from . import views

from .views import UserRegisterAPI,  UserLoginAPI, UserLogoutAPI

urlpatterns = [
    path('', views.LoginView.as_view(), name=''),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass/', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('reset-pass/', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('api/user/register/', UserRegisterAPI.as_view(), name='registerApi'),
    path('api/user/login/', UserLoginAPI.as_view(), name='loginApi'),
    # path('api/user/', UserView.as_view(), name='userView'),
    path('api/user/logout/', UserLogoutAPI.as_view(), name='logoutApi'),
]
