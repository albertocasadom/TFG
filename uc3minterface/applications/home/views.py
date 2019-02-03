from django.shortcuts import render
from django.http import serializers

# Create your views here.
from django.views.generic import (TemplateView , ListView, )

with open('/home/hacklberto/Telematics Degree/TFG/TFG/data.json','r') as listviewused:
	dataset = json.load(listviewused)

class IndexView(TemplateView):
	template_name = "home/index.html"

class TrainingList(ListView):
	template_name = "home/lista.html"
	queryset = dataset
	context_object_name = 'traininglist'
	print(queryset)