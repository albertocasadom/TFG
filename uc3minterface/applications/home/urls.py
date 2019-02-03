from django.urls import path, re_path

from . import views

app_name = "home_app"

urlpatterns = [ path('home', views.IndexView.as_view(), name = "index"),
path('traininglist', views.TrainingList.as_view(), name = "list")]