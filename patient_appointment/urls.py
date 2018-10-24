from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^add/$', views.schedule_appointmet, name="create_appointment"),
    url(r'^dentist_schedules/$', views.schedule_list, name="dentist_schedulelist"),
    url(r'^today/$', views.today_appointments,name="today_appointments"),
    url(r'^upcoming/$', views.upcoming_appointments, name='upcoming_appointments'),
    url(r'^all/$', views.all_appointment, name='all_appointments'),
    url(r'^search/$', views.search_appointment_by_contact_numer, name='appointment_search_by_contact_number'),
    url(r'^dentist/add/$', views.unregistered_appointment, name="add_unregistered_appointment"),
    url(r'^dentist/schedules/$', views.dentist_schedule_list, name="dentist_schedules"),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_appointment, name="edit_apppointment"),
]