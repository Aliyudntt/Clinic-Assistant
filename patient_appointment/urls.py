from django.urls import path

from . import views


urlpatterns = [
    path('add/', views.schedule_appointment, name="create_appointment"),
    path('appointment/dentist_schedules', views.dentist_schedules, name="schedules"),
    path('today/', views.today_appointments, name="today_appointments"),
    path('upcoming/', views.upcoming_appointments, name='upcoming_appointments'),
    path('all/', views.all_appointment, name='all_appointments'),
    path('search/', views.search_appointment_by_contact_numer, name='appointment_search_by_contact_number'),
    path('dentist/add/', views.unregistered_appointment, name="add_unregistered_appointment"),
    path('dentist/schedules/', views.dentist_schedule_list, name="dentist_schedules"),
    path('appointment/edit/<int:id>/', views.edit_appointment, name="edit_appointment"),
]