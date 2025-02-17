from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from medical.forms import CreateAppointmentForm, CreateAvailableDayForm, CreateLocationForm
from medical.models import Appointment, AvailableDay, Doctor, Location, Patient
from django.contrib.auth.mixins import UserPassesTestMixin
from utils.get_form_errors import get_form_errors
from django.core.exceptions import ValidationError
# Create your views here.

class CreateLocation(UserPassesTestMixin, View):
    def test_func(self):
        self.doctor = Doctor.objects.filter(user=self.request.user)
        return self.doctor.exists()

    def handle_no_permission(self):
        messages.error(
            self.request, "You can't access this page.")
        return redirect("home")

    def get(self, request):
        form = CreateLocationForm()
        context = {"form": form}
        return render(request, 'medical/doctor/create-location.html', context)

    def post(self, request):
        form = CreateLocationForm(request.POST)

        if not form.is_valid():
            messages.error(request, "invalid form")
            return redirect("create_doctor_location")

        location = Location(doctor=self.doctor.first(), **form.cleaned_data)
        location.save()
        messages.success(request, "Clinic created successfully")

        return redirect("create_doctor_location")


class CreateAvailableDay(UserPassesTestMixin, View):
    def test_func(self):
        id = self.kwargs.get("id")
        self.doctor = Doctor.objects.filter(user=self.request.user)
        self.location = Location.objects.filter(
            id=id, doctor=self.doctor.first())
        return self.doctor.exists() and self.location.exists()

    def handle_no_permission(self):
        messages.error(
            self.request, "You can't access this page.")
        return redirect("home")

    def get(self, request, id):
        form = CreateAvailableDayForm(location_id=id)
        context = {"form": form}
        booked_days = AvailableDay.objects.filter(
            location=id)
        if len(booked_days) == 7:
            return redirect("view_available_day", id=id)

        return render(request, 'medical/doctor/create-available-day.html', context)

    def post(self, request, id):
        form = CreateAvailableDayForm(id, request.POST)
        if not form.is_valid():
            errors = get_form_errors(form)
            messages.error(request, f"invalid form: {', '.join(errors)}")
            return redirect('create_available_day', id=id)

        available_day = AvailableDay(
            location=self.location.first(), **form.cleaned_data)
        available_day.save()
        messages.success(request, "Available day created successfully")

        return redirect('create_available_day', id=id)


class ViewBookedDays(UserPassesTestMixin, View):
    def test_func(self):
        id = self.kwargs.get("id")
        self.doctor = Doctor.objects.filter(user=self.request.user)
        self.location = Location.objects.filter(
            id=id, doctor=self.doctor.first())
        return self.doctor.exists() and self.location.exists()

    def handle_no_permission(self):
        messages.error(
            self.request, "You can't access this page.")
        return redirect("home")

    def get(self, request, id):
        booked_days = AvailableDay.objects.filter(
            location=self.location.first())
        return render(request, 'medical/doctor/view-booked-days.html', {"booked_days": booked_days})


class CreateAppointment(UserPassesTestMixin, View):
    def test_func(self):
        return Patient.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        messages.error(
            self.request, "You can't access this page.")
        return redirect("home")


    def get(self, request, id):
        form = CreateAppointmentForm(id, request.user)
        if not form.available_days:
            messages.error(request, f"No available days to reverse")
            return redirect('home')

        context = {'form': form}
        return render(request, 'medical/patient/create-appointment.html', context)

    def post(self, request, id):
        form = CreateAppointmentForm(id, request.user, request.POST)
        if not form.is_valid():
            errors = get_form_errors(form)
            messages.error(request, f"invalid form: {', '.join(errors)}")
            return redirect('create_appointment', id=id)

        target_day = form.cleaned_data['day']
        patient = Patient.objects.get(user=request.user)
        try:
            appointment = Appointment(day=target_day, patient=patient)
            appointment.save()
            messages.success(request, "Appointment Reversed Successfully")
            return redirect('home')

        except ValidationError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('create_appointment', id=id)
