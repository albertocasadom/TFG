from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
	template = loader.get_template('home.html')
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	context = { 'data':data}
	return HttpResponse(template.render(context, request))

def logout_view(request):
	template = loader.get_template('socialauth/logout.html')
	context = {}
	logout(request)
	return HttpResponse(template.render(context,request))

def login(request):
	template = loader.get_template('socialauth/login.html')
	login(request)
	context = {}
	return HttpResponse(template.render(context,request))
