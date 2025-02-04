from django.urls import path
from .views import Login, Logout, Register, SendResetCode

urlpatterns = [
  path("register/", Register.as_view(), name="register"),
  path("login/", Login.as_view(), name="login"),
  path("logout/", Logout.as_view(), name="logout"),
  path("send-reset-code/", SendResetCode.as_view(), name="send-reset-code"),
  
]