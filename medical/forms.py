from django.forms import ModelForm
from django.shortcuts import redirect
from medical.models import Appointment, AvailableDay, Location
from .utils import days_of_week
from django.contrib import messages

class CreateLocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ('doctor',)


class CreateAvailableDayForm(ModelForm):
    class Meta:
        model = AvailableDay
        exclude = ('current_appointments', 'location')

    def __init__(self, location_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if location_id:
            booked_days = AvailableDay.objects.filter(
                location=location_id).values_list('day_of_week', flat=True)
            self.fields['day_of_week'].choices = [
                (day, label) for day, label in days_of_week if day not in booked_days
            ]


class CreateAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('day',)

    def __init__(self, location_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if location_id:
            # Get all days the user has already booked
            booked_days = set(
                Appointment.objects.filter(day__location=location_id, patient__user=user)
                .values_list('day', flat=True)
            )

            # Get available days excluding already booked ones
            available_days = AvailableDay.objects.filter(location=location_id).exclude(id__in=booked_days)
            self.available_days = available_days
            
            self.fields['day'].choices = [
                (day.id, f'{day.get_day_of_week_display()}, from {day.get_time_12(day.time_from)} to {day.get_time_12(day.time_to)}') for day in available_days]
