from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contactUs/', views.contactUs),
    path('doctors/', views.doctors),
    path('diagnosis/', views.diagnosis),
    path('personal-care/', views.personal_care),
    path('services/', views.services),
    path('news/', views.news),
    path('treatment/', views.treatment),
    path('gallary/', views.gallary),
]