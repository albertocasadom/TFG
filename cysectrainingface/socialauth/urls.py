from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from socialauth.views import found, logout_view, search, showtraining,advancedsearch, advancedfound,usefulinfo,aboutus
urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'socialauth/login.html'), name = 'login'),
    url(r'^logout/$', logout_view, name = 'logout'),
    path('', search, name = 'search'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^found/', found, name='found'),
    url(r'^show/$', showtraining, name = 'showtraining'),
    url(r'^advanced/$', advancedsearch, name = 'advanced'),
    url(r'^advancedfound/$', advancedfound, name = 'advancedfound'),
    url(r'^usefulinfo/$', usefulinfo, name='usefulinfo'),
    url(r'^aboutus/$', aboutus, name='aboutus'),
]
