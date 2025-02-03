from django.contrib import admin
from .models import AvailableDay, Doctor, Location, Patient, Appointment

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Location)
admin.site.register(AvailableDay)
admin.site.register(Patient)
admin.site.register(Appointment)
