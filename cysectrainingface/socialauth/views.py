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

def get_checkbox_repeated(dataset):
	datafound = []
	repeated = []
	keys = list(dataset.keys())
	print("---- get_dataset_repeats ----")
	if len(keys) == 0:
			return (repeated,-1)
	if len(keys) == 1:
		for data in dataset[keys[0]]:
			datafound.append(data)
		print("Número de elementos encontrados: {0}".format(len(datafound)))
		return (datafound,0)
	else:
		for x in range(0,len(keys)):
			if (x+1 == len(keys)):
				break
			for datasetobj in dataset[keys[x]]:
				for datasetcompare in dataset[keys[x+1]]:
					if datasetobj == datasetcompare:
						if datasetobj not in repeated:
							repeated.append(datasetobj)
		print("Número de elementos encontrados: {0}".format(len(repeated)))
		
		return (repeated,0)

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
	advancedsearchtrs = {}
	alllogictrs = {}
	checkboxclicked = 0
	parameters = list(request.POST.keys())
	
	print(parameters)
	for param in parameters:
		if "-" in param:
			fixedsearch.append(param)
	print(fixedsearch)
	for p in fixedsearch:
		print("{0} eliminado".format(p))
		parameters.remove(p)
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
			checkboxclicked+= 1

	if checkboxclicked != 0:		
		andtrainings = get_checkbox_repeated(dataset)
	else:
		andtrainings = (data['resources'],0)

	if andtrainings[1] == 0:
		data['resources'] = andtrainings[0]

		parameters.remove('csrfmiddlewaretoken')
		parameters.sort()
		print(parameters)
		x = len(parameters)-1
		print("La longitud es: {0}".format(x))

		for parameter in parameters:
			parameterlist = ['','','']
			if 'text' in parameter:
				splitparameter = parameter.split('text')
				parameterlist[0] = parameter
				if splitparameter[1] != '':
					for p in parameters:
						if splitparameter[1] in p and "content" in p:
							parameterlist[1] = p
						elif splitparameter[1] in p and "filter" in p:
							parameterlist[2] = p
				else:
					for p in parameters:
						if "content" in p:
							parameterlist[1] = p
						elif "filter" in p:
							parameterlist[2] = p
				groupsearch.append(parameterlist)
		
		print(groupsearch)
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
									advancedsearchtrs['logic'] = logic
									advancedsearchtrs['resources'] = result
								else:
									for el in training[key]:
										if el.lower() in value:
											result.append(training)
											break
										else: 
											continue
									advancedsearchtrs['logic'] = logic
									advancedsearchtrs['resources'] = result
							else:
								continue
					alllogictrs[x] = advancedsearchtrs
							
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
					context['data']=result
					context['text']= value

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
						context['data'] = result
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

		for x in range(1,len(alllogictrs)+1):
			resultr = []
			if alllogictrs[x]['logic'] == "or":
				resultr += alllogictrs[x]['resources']
				if x+1 in range(1,len(alllogictrs)+1):
					resultr += alllogictrs[x+1]['resources']
		print(resultr)

		return HttpResponse(template.render(context, request))
	else:
		return HttpResponse(template.render(context,request))

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