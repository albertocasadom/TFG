from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
import re
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_filters():
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	searchfilter = []
	values = []
	pairvalues = []
	for resources in data['resources']:
		keys = list(resources.keys())
		for key in keys:
			if key in searchfilter:
				continue
			else:
				searchfilter.append(key)
	for key in searchfilter:
		values = []
		for training in data['resources']:
			if key in list(training.keys()):
				if training[key] in values:
					continue
				else:
					values.append(training[key])
		if len(values) < 5:
			pairvalues.append((key,values))

	for valuekey in pairvalues:
		searchfilter.remove(valuekey[0])

	context = {'filter':searchfilter, 'pairvalues':pairvalues, 'length': len(pairvalues)}
	return context

def get_dataset_repeats(dataset):
	datafound = []
	repeated = []
	keys = list(dataset.keys())
	print("---- get_dataset_repeats ----")
	if len(keys) == 1:
		for data in dataset[keys[0]]:
			datafound.append(data)
		print("Número de elementos encontrados: {0}".format(len(datafound)))
		for element in datafound:
			print("REPEATED: {0}".format(element))
		return datafound
	else:
		for x in range(0,len(keys)):
			if (x+1 == len(keys)):
				break
			print("La clave es: {0}".format(keys[x]))
			for datasetobj in dataset[keys[x]]:
				for datasetcompare in dataset[keys[x+1]]:
					if datasetobj == datasetcompare:
						if datasetobj not in repeated:
							repeated.append(datasetobj)
		print("Número de elementos encontrados: {0}".format(len(repeated)))
		for element in repeated:
			print("REPEATED: {0}".format(element))

		return repeated


def search(request):
	template = loader.get_template('search.html')
	context = get_filters()
	return HttpResponse(template.render(context,request))
def found(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	template = loader.get_template('found.html')
	getfilter = request.POST.get('filter')
	gettext = request.POST.get('text').lower()
	result = []
	trainingnames = []
	text = []
	if getfilter != 'word':
		for training in data['resources']:
			#Preguntar primero si el training tiene la clave.
			keys = list(training.keys())
			if getfilter in keys:
			#Separar palabras de búsqueda
				if type(training[getfilter]) != list:
					if gettext in training[getfilter].lower():
						result.append(training)
						break
					else:
						continue
				else:
					for el in training[getfilter]:
						if el.lower() == gettext:
							result.append(training)
							break
						else: 
							continue
							
			else:
				continue
		context = {'data':result}
	else:
		numberepeated = []
		ENISA_DIR = os.walk(os.path.join(BASE_DIR,'../EnisaFiles'))
		for dirs in ENISA_DIR:
			file = os.path.join(dirs[0],'mainwordfile.txt')
			if os.path.exists(file):
				with open(file,'r') as wordsfile:
					repeated = 0
					for l in wordsfile:
						match = re.findall(gettext,l.lower())
						repeated = len(match)
					if repeated > 0:
						dirsname = dirs[0].split('EnisaFiles/')
						trainingnames.append((dirsname[1],repeated))
		SEED_DIR = os.walk(os.path.join(BASE_DIR,'../SeedFiles'))
		for dirs in SEED_DIR:
			file = os.path.join(dirs[0],'mainwordfile.txt')
			if os.path.exists(file):
				with open(file,'r') as wordsfile:
					repeated = 0
					for l in wordsfile:
						match = re.findall(gettext,l.lower())
						repeated = len(match)
					if repeated > 0:
						dirsname = dirs[0].split('SeedFiles/')
						trainingnames.append((dirsname[1],repeated))
		for training in data['resources']:
			for tr in trainingnames:
				if tr[0] == training['title']:
					result.append((training,tr[1]))
					result.sort(key=lambda numword: numword[1], reverse = True) 
		template = loader.get_template('foundtext.html')
		context = {'data':result, 'text': gettext}
	return HttpResponse(template.render(context, request))

def advancedsearch(request):
	template = loader.get_template('advancedsearch.html')
	context = get_filters()
	return HttpResponse(template.render(context,request))

def advancedfound(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	lenfixedsearch = 0
	template = loader.get_template('found.html')
	context = {}
	dataset = {}
	groupsearch = []
	finalsearch = []
	result = []
	trainingnames = []
	fixedsearch = []
	parameters = list(request.POST.keys())
	print(parameters)
	lenfixedparameters = parameters[1].split("-")
	lenfixed = int(lenfixedparameters[1])
	x = lenfixed
	while(x != 0):
		fixedsearch.append(parameters[x])
		x = x-1

	while(len(fixedsearch) != 0):
		key = fixedsearch.pop()
		value = request.POST.get(key)
		key = key.split('-')[0]
		print("La clave es: {0} y el valor: {1}".format(key,value))
		if(value != "Any"):
			dataset[key] = []
			for training in data['resources']:
				if key in list(training.keys()):
					if training[key] == value:
						if training not in dataset[key]:
							dataset[key].append(training)

	with open('test.json','w') as out:
		json.dump(dataset,out,indent=4)

	context['checkbox'] = get_dataset_repeats(dataset)

	x = len(parameters)

	while(x != 1 + lenfixed):
		auxparameters = parameters
		groupsearch.append((auxparameters.pop(),auxparameters.pop(), auxparameters.pop()))
		x = len(auxparameters)

	groupsearch.reverse()
	for parameter in groupsearch:
		search = ["","","",""]
		if "or" in parameter[0]:
			search[0] = "or"
		else:
			search[0] = "and"

		search[3] = request.POST.get(parameter[0]).lower()
		search[2] = request.POST.get(parameter[1])
		search[1] = request.POST.get(parameter[2])
		finalsearch.append(search);

	x = len(finalsearch)

	while(x != 0):
		key = finalsearch[x-1][1]
		value = finalsearch[x-1][3].lower()
		logic = finalsearch[x-1][0]
		contains = finalsearch[x-1][2]
		print(key)
		print(value)
		print(logic)
		print(contains)
		x = x-1
		if contains == "contains":
			if key != "word":
				#print(key)
				for training in data['resources']:
				#Preguntar primero si el training tiene la clave.
					if training not in result:
						keys = list(training.keys())
						if key in keys:
						#Separar palabras de búsqueda
							if type(training[key]) != list:
								text = value.split(" ")
								for word in text:
									if word in training[key].lower():
										result.append(training)
										break
									else:
										continue
							else:
								for el in training[key]:
									if el.lower() in value:
										result.append(training)
										break
									else: 
										continue
						else:
							continue
						context = {'data':result}
			else:
				numberepeated = []
				ENISA_DIR = os.walk(os.path.join(BASE_DIR,'../EnisaFiles'))
				for dirs in ENISA_DIR:
					file = os.path.join(dirs[0],'mainwordfile.txt')
					if os.path.exists(file):
						with open(file,'r') as wordsfile:
							repeated = 0
							for l in wordsfile:
								match = re.findall(value,l.lower())
								repeated = len(match)
							if repeated > 0:
								dirsname = dirs[0].split('EnisaFiles/')
								trainingnames.append((dirsname[1],repeated))
				SEED_DIR = os.walk(os.path.join(BASE_DIR,'../SeedFiles'))
				for dirs in SEED_DIR:
					file = os.path.join(dirs[0],'mainwordfile.txt')
					if os.path.exists(file):
						with open(file,'r') as wordsfile:
							repeated = 0
							for l in wordsfile:
								match = re.findall(value,l.lower())
								repeated = len(match)
							if repeated > 0:
								dirsname = dirs[0].split('SeedFiles/')
								trainingnames.append((dirsname[1],repeated))
				for training in data['resources']:
					for tr in trainingnames:
						if tr[0] == training['title'] and (training,tr[1]) not in result:	
							result.append((training,tr[1]))
							result.sort(key=lambda numword: numword[1], reverse = True) 
				template = loader.get_template('foundtext.html')
				context = {'data':result, 'text': value}

		elif contains == "is":
			if key != "word":
				print(key)
				for training in data['resources']:
				#Preguntar primero si el training tiene la clave.
					keys = list(training.keys())
					if key in keys:
					#Separar palabras de búsqueda
						if type(training[key]) != list:
							if value == training[key].lower():
								result.append(training)
							else:
								continue
						else:
							for el in training[key]:
								if el.lower() == value:
									result.append(training)
								else: 
									continue
					else:
						continue
					context = {'data':result}
			else: 
				numberepeated = []
				ENISA_DIR = os.walk(os.path.join(BASE_DIR,'../EnisaFiles'))
				for dirs in ENISA_DIR:
					file = os.path.join(dirs[0],'mainwordfile.txt')
					if os.path.exists(file):
						with open(file,'r') as wordsfile:
							stringread = wordsfile.read().lower()
							match = stringread.find(value)
							if match != -1:
								dirsname = dirs[0].split('EnisaFiles/')
								trainingnames.append(dirsname[1])
									
				SEED_DIR = os.walk(os.path.join(BASE_DIR,'../SeedFiles'))
				for dirs in SEED_DIR:
					file = os.path.join(dirs[0],'mainwordfile.txt')
					if os.path.exists(file):
						with open(file,'r') as wordsfile:
							stringread = wordsfile.read()
							match = stringread.find(value)
							if match != -1:
								dirsname = dirs[0].split('SeedFiles/')
								trainingnames.append(dirsname[1])
				for training in data['resources']:
					for tr in trainingnames:
						if tr == training['title']:
							if training not in result:
								result.append(training)
				template = loader.get_template('found.html')
				context['data'] = result
				context['text'] = value
	
	return HttpResponse(template.render(context, request))

def showtraining(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	template = loader.get_template('showtraining.html')
	trainingname = request.GET.get('training')
	context = {}
	print(trainingname)
	for tr in data['resources']:
		if tr['title'] == trainingname:
			print(tr)
			context = {'training':tr, 'test':'test'}
	return HttpResponse(template.render(context,request))

def logout_view(request):
	logout(request)
	return render(request,'socialauth/logout.html')