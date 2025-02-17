from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from authentication.models import User
from medical.models import Doctor, Patient
from utils.decorators.user_not_auth import user_not_authenticated
from .forms import ChangePasswordResetCodeForm, LoginForm, RegisterForm, PasswordResetCodeForm
from django.contrib.auth import authenticate, login, logout
import random
from cryptography.fernet import Fernet
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
import os

ENCRYPTION_KEY = bytes(os.getenv('ENCRYPTION_KEY'), 'utf-8')
fernet = Fernet(ENCRYPTION_KEY)

# @method_decorator(csrf_exempt, name='dispatch')
class Register(View):
    @method_decorator(user_passes_test(user_not_authenticated, login_url="home"))
    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        # create user
        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data['account_type']
            if account_type == 'doctor':
                Doctor.objects.create(user=user)
            else:
                Patient.objects.create(user=user)

            # login
            user = authenticate(
                username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)

            # response
            messages.success(request, "User added successfully")
            return redirect("home")

        messages.error(request, "Something went wrong")
        return render(request, "auth/register.html", {"form": form})


class Login(View):
    @method_decorator(user_passes_test(user_not_authenticated, login_url="home"))
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {"form": form})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect("home")
        else:
            messages.error(request, "Email or password is incorrect")
            return redirect("login")


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class PasswordResetCode(View):
    @method_decorator(user_passes_test(user_not_authenticated, login_url="home"))
    def get(self, request):
        form = PasswordResetCodeForm()
        context = {"form": form}
        return render(request, 'auth/forget-password.html', context)

    def post(self, request):
        form = PasswordResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the user exists with the provided email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect("forget_password")

            # Generate a random reset code (6 digits)
            reset_code = str(random.randint(100000, 999999))
            enc_reset_code = fernet.encrypt(reset_code.encode())

            encoded_reset_code = str(enc_reset_code, "utf-8")

            # حفظ البيانات في قاعدة البيانات
            user.password_reset_code = encoded_reset_code
            user.reset_code_created_at = timezone.now()
            user.save()

            # save email in session
            request.session["reset_email"] = email

            # send email
            email_body = f"""
            <p>Hello {user.get_full_name()},</p>
            <p>You requested a password reset for your account.</p>
            <p>Your reset code is: <strong>{reset_code}</strong></p>
            <p>Please use this code as soon as possible.</p>
            """

            send_mail(
                subject="Password Reset Code",
                from_email=None,
                message="",
                recipient_list=[email],
                html_message=email_body,
            )

            messages.success(
                request, "A reset code has been sent to your email.")
            return redirect("change_forget_password")

        messages.error(request, "Invalid form submission.")
        return redirect("forget_password")


class ChangeForgetPassword(View):
    @method_decorator(user_passes_test(user_not_authenticated, login_url="home"))
    def get(self, request):
        if 'reset_email' not in request.session:
            return redirect("forget_password")

        form = ChangePasswordResetCodeForm(request=request)
        context = {"form": form}
        return render(request, 'auth/change-password-reset-code.html', context)

    def post(self, request):
        form = ChangePasswordResetCodeForm(request.POST)
        print(form.data)
        if not form.is_valid():
            messages.error(request, "Invalid form submission.")
            return redirect("change_forget_password")

        email = form.cleaned_data['email']
        reset_code = form.cleaned_data['code']
        new_password = form.cleaned_data['new_password']

        user = self.get_user(email)
        if not user:
            messages.error(request, "User not found, Send reset code again")
            return redirect("forget_password")

        if not self.is_valid_reset_code(user, reset_code):
            messages.error(request, "Invalid or expired reset code")
            return redirect("change_forget_password")

        self.update_user_password(user, new_password)
        messages.success(request, "Password changed successfully")
        return redirect("login")

    def get_user(self, email: str):
        """Retrieve user by email or return None if not found."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def is_valid_reset_code(self, user: User, reset_code: str):
        """Check if reset code is valid and not expired."""
        try:
            enc_reset_code = bytes(user.password_reset_code, "utf-8")
            plain_reset_code = fernet.decrypt(enc_reset_code).decode()
            is_expired = not user.reset_code_created_at or \
                user.reset_code_created_at + \
                timedelta(minutes=15) < timezone.now()
            return plain_reset_code == reset_code and not is_expired
        except Exception:
            return False

    def update_user_password(self, user: User, new_password: str):
        """Update user password and reset password reset fields."""
        user.set_password(new_password)
        user.password_reset_code = None
        user.reset_code_created_at = None
        user.save()
