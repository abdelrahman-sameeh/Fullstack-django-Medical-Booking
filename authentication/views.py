from django.shortcuts import render, redirect
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib import messages
from medical.models import Doctor, Patient
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

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
          user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
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