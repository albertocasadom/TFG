from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from socialauth.views import found, logout_view, search, showtraining,advancedsearch, advancedfound

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'socialauth/login.html'), name = 'login'),
    url(r'^logout/$', logout_view, name = 'logout'),
    url(r'^search/', search, name = 'search'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^found/', found, name='found'),
    url(r'^show/$', showtraining, name = 'showtraining'),
    url(r'^advanced/$', advancedsearch, name = 'advanced'),
    url(r'^advancedfound/$', advancedfound, name = 'advancedfound'),
]
