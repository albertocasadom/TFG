from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import os
import json
def index(request):
	user = "medinaca"
	template = loader.get_template('applications/index.html')
	with open('/home/hacklberto/Telematics Degree/TFG/TFG/data.json','r') as datafile:
		data = json.load(datafile)
	context = { 'data':data}
	return HttpResponse(template.render(context, request))

