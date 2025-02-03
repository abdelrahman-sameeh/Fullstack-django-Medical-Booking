from django.db import models
from authentication.models import User
from .utils import egypt_provinces, days_of_week
import datetime
# Create your models here.

class Doctor(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class Location(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    government = models.CharField(
        max_length=2, choices=egypt_provinces, default="CA")
    details = models.TextField(max_length=200, blank=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.get_government_display()} - {self.details}"


class AvailableDay(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=2, choices=days_of_week)
    time_from = models.TimeField(blank=True, default=datetime.time(15, 0))
    time_to = models.TimeField(blank=True, default=datetime.time(21, 0))
    max_appointments = models.PositiveIntegerField(default=0)
    current_appointments = models.PositiveIntegerField(default=0)

    def is_available(self):
        """
        إذا تم الوصول إلى الحد الأقصى للكشوفات لهذا اليوم.
        """
        return self.current_appointments <= self.max_appointments

    def increment_appointments(self):
        """
        زيادة عدد الكشوفات لهذا اليوم.
        """
        if self.is_available():
            self.current_appointments += 1
            self.save()
            return True
        return False

    def get_time_12(self, time: datetime.time):
        hours = time.hour % 12 or 12
        min = f"0{time.minute}" if time.minute < 10 else time.minute
        sign = "PM" if time.hour >= 12 else "AM"
        return f"{hours}:{min} {sign}"

    def __str__(self):
        return f"from {self.get_time_12(self.time_from)} to {self.get_time_12(self.time_to)} - {self.get_day_of_week_display()} - {self.location.get_government_display()} - {self.location.details} - Dr. {self.location.doctor.user.get_full_name()}"


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"P- {self.user.get_full_name()}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True)
    day = models.ForeignKey(AvailableDay, on_delete=models.CASCADE, blank=True)
    appointment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Appointment for {self.patient.user.get_full_name()} with Dr. {self.doctor.user.get_full_name()} on {self.day.get_day_of_week_display()} - {self.appointment_date}"


