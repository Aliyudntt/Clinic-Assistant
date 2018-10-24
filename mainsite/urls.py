from django.conf.urls import url


from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^contactUs/$',views.contactUs),
    url(r'^dentists/$',views.dentists),
    url(r'^diagnosis/$', views.diagnosis),
    url(r'^personal-care/$',views.personal_care),
    url(r'^services/$',views.services),
    url(r'^news/$', views.news),
    url(r'^treatment/$', views.treatment),
    url(r'^gallary/$', views.gallary),
]