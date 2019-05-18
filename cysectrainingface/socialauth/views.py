from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout
from django.conf import settings
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

	legend = []
	for valuekey in pairvalues:
		for training in data['resources']:
			keys = list(training.keys())
			if valuekey[0] not in keys:
				if (valuekey[0],training['source']) not in legend:
					print(valuekey[0])
					print(training['source'])
					legend.append((valuekey[0],training['source']))
				

	context = {'filter':searchfilter, 'pairvalues':pairvalues, 'length': len(pairvalues), 'legend':legend}
	return context

def basic_training_search(value,data):
	result = []
	trainingnames = []
	text = []
	for training in data['resources']:
		#Preguntar primero si el training tiene la clave.
		keys = list(training.keys())
		for key in keys:
		#Separar palabras de búsqueda
			if type(training[key]) == str:
				if value.lower() in training[key].lower() and training not in result:
					result.append(training)
				else:
					continue

			elif type(training[key]) == int:
				if value == str(training[key]):
					result.append(training)
			
			elif type(training[key]) == list:
				for el in training[key]:
					if el.lower() == value and training not in result:
						result.append(training)
					else: 
									continue
	return result

def basic_key_search(key,value,typesearch,logic,data):
	advancedsearchtrs = []
	result = []
	if typesearch == "contains":
		if key != "word":
			for training in data['resources']:
			#Preguntar primero si el training tiene la clave.
				if training not in result:
					keys = list(training.keys())
					if key in keys:
					#Separar palabras de búsqueda
						if type(training[key]) == str:
							if value.lower() in training[key].lower() and training not in result:
								result.append(training)
							else:
								continue

						elif type(training[key]) == int:
							if int(value) == training[key]:
								result.append(training)
						
						elif type(training[key]) == list:
							for el in training[key]:
								if el.lower() == value and training not in result:
									result.append(training)
								else: 
									continue
								
			advancedsearchtrs.append(result)
			advancedsearchtrs.insert(0,logic)
			return advancedsearchtrs
			#return result
		else:
			result = search_word_in_files(value,data)
			resultfiles = []
			for tr in result:
				resultfiles.append(tr[0])
				print("File {0}".format(tr[0]['title']))
				advancedsearchtrs.append(resultfiles)
			advancedsearchtrs.insert(0,logic)
			return advancedsearchtrs
			#return result
	elif typesearch == "is":
		if key != "word":
			for training in data['resources']:
			#Preguntar primero si el training tiene la clave.
				if training not in result:
					keys = list(training.keys())
					if key in keys:
					#Separar palabras de búsqueda
						if type(training[key]) != list:
							if value == training[key].lower():
								result.append(training)
								print(training['title'])
							else:
								continue
						else:
							for el in training[key]:
								if el.lower() == value:
									result.append(training)
									print(training['title'])
								else: 
									continue
					else:
						continue
			advancedsearchtrs.append(result)
			advancedsearchtrs.insert(0,logic)
			return advancedsearchtrs
		else: 
			result = search_is_word_files(word,data)
			resultfiles = []
			for tr in result:
				resultfiles.append(tr[0])
				advancedsearchtrs.append(resultfiles)
				advancedsearchtrs.insert(0,logic)
			return advancedsearchtrs


def search_word_in_files(word,data):
	trainingnames = []
	result = []
	ENISA_DIR = os.walk(os.path.join(BASE_DIR,'../EnisaFiles'))
	for dirs in ENISA_DIR:
		file = os.path.join(dirs[0],'mainwordfile.txt')
		if os.path.exists(file):
			with open(file,'r') as wordsfile:
				repeated = 0
				for l in wordsfile:
					match = re.findall(word,l.lower())
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
					match = re.findall(word,l.lower())
					repeated = len(match)
				if repeated > 0:
					dirsname = dirs[0].split('SeedFiles/')
					trainingnames.append((dirsname[1],repeated))
	for training in data['resources']:
		for tr in trainingnames:
			if tr[0] == training['title']:
				result.append([training,tr[1]])
				result.sort(key=lambda numword: numword[1], reverse = True)

	return result

def search_is_word_files(word,data):
	numberepeated = []
	result =[] 
	trainingnames = []
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
	return result

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

def get_post_parameters(parameters):
	groupsearch = []
	x = len(parameters)
	while (x != 0):
		parameterlist = [parameters.pop(),parameters.pop(),parameters.pop(),parameters.pop()]
		print(parameterlist)
		groupsearch.append(parameterlist)
		x = len(parameters)
	groupsearch.sort()
	return groupsearch

def search(request):
	template = loader.get_template('search.html')
	context = get_filters()
	return HttpResponse(template.render(context,request))
def found(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	result = []
	resultfiles = []
	template = loader.get_template('found.html')
	text = request.POST.get('text').lower()
	trainings = basic_training_search(text,data)
	result.append((text.upper(),trainings))
	filestr = search_word_in_files(text,data)
	resultfiles.append((text.upper(),filestr))
	splittext = text.split(" ")
	'''if (len(splittext) > 1):
		for word in splittext:
			trainings = basic_training_search(word,data)
			filestr = search_word_in_files(word,data)
			result.append((word.upper(),trainings))
			resultfiles.append((word.upper(),filestr))'''

	context = {'data':result, 'files':resultfiles}
	return HttpResponse(template.render(context, request))

def advancedsearch(request):
	template = loader.get_template('advancedsearch.html')
	context = get_filters()
	return HttpResponse(template.render(context,request))

def advancedfound(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	lenfixedsearch = 0
	resultr= []
	template = loader.get_template('found.html')
	context = {}
	dataset = {}
	groupsearch = []
	finalsearch = []
	result = []
	trainingnames = []
	fixedsearch = []
	advancedsearchtrs = []
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
		parametersaux = parameters
		parametersaux.remove('csrfmiddlewaretoken')
		parametersaux.sort()
		print(parametersaux)
		groupsearch = get_post_parameters(parametersaux)
		print("Groupsearch es: {0}".format(groupsearch))
		for parameter in groupsearch:
			search = ["","","",""]
			
			search[0] = request.POST.get(parameter[3])
			search[3] = request.POST.get(parameter[0]).lower()
			search[2] = request.POST.get(parameter[1])
			search[1] = request.POST.get(parameter[2])
			finalsearch.append(search);

		finalsearch.reverse()
		x = len(finalsearch)
		print(finalsearch)
		numlogics = x
		print("LA LONGITUD DE FINALSEARCH ES: {0}".format(x))
		advancedlogic = []
		query = "The search: "
		while(x != 0):
			key = finalsearch[x-1][1]
			value = finalsearch[x-1][3].lower()
			contains = finalsearch[x-1][0]
			logic = finalsearch[x-1][2]
			result = []
			print("-->LA BÚSQUEDA ({3}) '{2}' CON CLAVE: {0} Y VALOR: {1} DEVUELVE...".format(key,value,logic.upper(),contains))	
			result = basic_key_search(key,value,contains,logic,data)
			
			advancedsearchtrs.append(result[1])
			advancedlogic.append(result[0])
			x = x-1
			query += logic + " " + key + " " + contains + " " + value + " " 

		query+= "has given the following results"
		indexsplit = []
		element = 0
		while element < len(advancedlogic):
			if advancedlogic[element] == "or":
				indexsplit.append(element)
			element+=1

		for index in range(len(indexsplit)):
			if len(resultr) == 0:
				resultr.append(advancedsearchtrs[:indexsplit[index]])
			if index+1 in range(len(indexsplit)):
				resultr.append(advancedsearchtrs[indexsplit[index]:indexsplit[index+1]])
			else:
				resultr.append(advancedsearchtrs[indexsplit[index]:])

		for res in resultr:
			print("------------------")
			for tr in res:
				for training in tr:
					print(training['title'])
		andtrainings = []
		finalresultand = []
		finalresult = []
		alltrainings = []
		
		if(len(resultr) > 0):
			print("Longitud de resultr: {0}".format(len(resultr)))
			for andtrs in resultr:
				andtrainings = []
				numands = len(andtrs)
				print("Numero de ANDS: {0}".format(numands))
				for andresult in andtrs:
					print("Longitud de andresult: {0}".format(len(andresult)))
					for tr in andresult:
						andtrainings.append(tr)
				alltrainings.append([andtrainings,numands])	
		
			for res in alltrainings:
				for tr in res[0]:
					print()
					if res[0].count(tr) == res[1]:
						if tr not in finalresultand:
							finalresultand.append(tr)
			print("La longitud de todos los trainigs: {0}".format(len(alltrainings)))

		else:
			numands = len(advancedsearchtrs)
			print("Numero de ANDS: {0}".format(numands))
			for res in advancedsearchtrs:
				for tr in res:
					finalresult.append(tr)
			#print("Count of {0} = {1}".format(tr['title'],res.count(tr)))
			for tr in finalresult:
				if finalresult.count(tr) == numands:
					if tr not in finalresultand:
						finalresultand.append(tr)



		template = loader.get_template('foundlogic.html')
		context['data'] = finalresultand
		context['text'] = query
		
		return HttpResponse(template.render(context, request))
	else:
		return HttpResponse(template.render(context,request))

def showtraining(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	template = loader.get_template('showtraining.html')
	trainingid = request.GET.get('id')
	context = {}
	trainingfiles = []
	files = []
	for tr in data['resources']:
		if str(tr['id']) == trainingid:
			training = tr
	rango = range(len(training['files']))
	linksname = []
	for x in rango:
		linksname.append([training['files'][x],training['urls'][x]])
	context = {'training': training, 'linksname':linksname}
	return HttpResponse(template.render(context,request))

def logout_view(request):
	logout(request)
	return render(request,'socialauth/logout.html')