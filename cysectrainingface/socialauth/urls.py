from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from socialauth.views import home, logout_view

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'socialauth/login.html')),
    url(r'^logout/$', logout_view, name = 'logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^$', home, name='home'),
]
