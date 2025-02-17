from django.urls import path

from medical.views import CreateAppointment, CreateLocation, CreateAvailableDay, ViewBookedDays

urlpatterns = [
  # doctor
  path("location/", CreateLocation.as_view(), name="create_doctor_location"),
  path("location/<int:id>/booked-days/", ViewBookedDays.as_view(), name="view_available_day"),
  path("location/<int:id>/available-days/", CreateAvailableDay.as_view(), name="create_available_day"),
  
  # patient
  path('location/<int:id>/appointment', CreateAppointment.as_view(), name='create_appointment'),
  
]