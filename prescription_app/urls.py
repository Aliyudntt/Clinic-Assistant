from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^medicines/$', views.medicinelist, name='medicine_list'),
    url(r'^medicine/add/', views.medicine_add, name='medicine_add'),
    url(r'tests/$', views.testlist, name='testlist'),
    url(r'^test/add/$', views.test_add, name='test_add'),
    url(r'^prescribe/(?P<appointment_id>[0-9]+)/$', views.prescription_add),
    url(r'^history/(?P<id>[0-9]+)/$', views.history_detail),
    url(r'^history/$',views.historylist),
    url(r'^pdf/(?P<id>[0-9]+)/$', views.to_pdf),
]