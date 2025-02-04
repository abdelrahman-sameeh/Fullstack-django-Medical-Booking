from django.shortcuts import render, redirect
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from setuptools import Command
from medical.models import Doctor, Patient
from .forms import LoginForm, RegisterForm, SendResetCodeForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail




# @method_decorator(csrf_exempt, name='dispatch')
class Register(View):
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

    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})


class Login(View):
    form = LoginForm()

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
            return render(request, 'auth/login.html', {"form": self.form})

    def get(self, request):
        return render(request, 'auth/login.html', {"form": self.form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class SendResetCode(View):
    def post(self, request):
        form = SendResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail("test", "testing message", None, [email], fail_silently=False)
        
        return self.get(request)

    def get(self, request):
        form = SendResetCodeForm()
        context = {"form": form}
        return render(request, 'auth/send-reset-code.html', context)

