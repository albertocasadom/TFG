from django.conf.urls import url
from APIfaceREST import views
urlpatterns = [
    url(r'^trainings/$', views.traininglist),
    #url(r'^test/$', views.test),
    #url(r'^series/(?P<pk>[0-9]+)/$', views.serie_detail),
]
