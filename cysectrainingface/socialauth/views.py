from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
import re
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def found(request):
	template = loader.get_template('found.html')
	getfilter = request.POST.get('filter')
	gettext = request.POST.get('text')
	result = []
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	if getfilter != 'word':
		for training in data['resources']:
			if gettext in training[getfilter]:
				result.append(training)
			else:
				continue
	else:
		ENISA_DIR = os.walk(os.path.join(BASE_DIR,'../EnisaFiles'))
		repeated = 0
		for dirs in ENISA_DIR:
			file = os.path.join(dirs[0],'mainwordfile.txt')
			if os.path.exists(file):
				with open(file,'r') as wordsfile:
					lines = wordsfile.readlines()
					for line in lines:
						words = line.split(' ')
						for w in words:
							repeated+=1
							dirsname = dirs[0].split(BASE_DIR)
							print(dirsname[1])

		print(repeated)
	context = {'data':result}
	return HttpResponse(template.render(context, request))

def logout_view(request):
	logout(request)
	return render(request,'socialauth/logout.html')

def search(request):
	template = loader.get_template('search.html')
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	searchfilter = []
	for resources in data['resources']:
		keys = list(resources.keys())
		for key in keys:
			if key in searchfilter:
				continue
			else:
				searchfilter.append(key)
	context = {'filter':searchfilter}
	return HttpResponse(template.render(context,request))