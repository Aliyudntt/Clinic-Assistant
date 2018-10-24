from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^dashboard/$', views.dashboard, name='dashboard_home'),
]