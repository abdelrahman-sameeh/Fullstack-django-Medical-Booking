from django.urls import path
from .views import ChangeForgetPassword, Login, Logout, Register, PasswordResetCode

urlpatterns = [
  path("register/", Register.as_view(), name="register"),
  path("login/", Login.as_view(), name="login"),
  path("logout/", Logout.as_view(), name="logout"),
  path("forget-password/", PasswordResetCode.as_view(), name="forget_password"),
  path("change-forget-password/", ChangeForgetPassword.as_view(), name="change_forget_password"),
  
]