from django.urls import path

from . import views

urlpatterns = [
    path('medicines/', views.medicinelist, name='medicine_list'),
    path('medicine/add/', views.medicine_add, name='medicine_add'),
    path('tests/', views.testlist, name='testlist'),
    path('test/add/', views.test_add, name='test_add'),
   # path('prescribe/<int:appointment_id>/', views.prescribe_view, name='prescribe'),
   # path('history/<int:id>/', views.history_view, name='history'),
    path('history/', views.historylist),
   # path('pdf/<int:id>/', views.pdf_view, name='pdf'),
]