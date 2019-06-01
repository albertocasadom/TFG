from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated  
import os
import json
import re
from socialauth import views


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def basic_training_search(word,data,key):
	print("La palabra introducida es: {0}".format(word))
	result = []
	trainingnames = []
	text = []
	print(key)
	if key != "word":
		for training in data['resources']:
			#Preguntar primero si el training tiene la clave.
			keys = list(training.keys())
			if key in keys:
				print(type(training[key]))
				if type(training[key]) == str:
					if word.lower() in training[key].lower() and training not in result:
						result.append(training)
					else:
						continue

				elif type(training[key]) == int:
					if int(word) == training[key]:
						result.append(training)
						
				elif type(training[key]) == list:
					for el in training[key]:
						if el.lower() == word and training not in result:
							result.append(training)
						else: 
							continue
	else:
		result = views.search_word_in_files(word,data)
	return result
class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def traininglist(request):
	with open(os.path.join(BASE_DIR, '../data.json'),'r') as datafile:
		data = json.load(datafile)
	keylist = ['word']
	#Obtiene todas las claves que hay en el fichero json
	for training in data['resources']:
		keys = training.keys()
		for key in keys:
			if key not in keylist:
				keylist.append(key)

	if request.method == 'POST':
		print(request.POST)
		parameters = list(request.POST.keys())
		print(parameters)
		jsonresult = {}
		if (len(parameters) == 1):
				if parameters[0] in keylist:
					print(request.POST.get(parameters[0]))
					jsonresult = {"resources": basic_training_search(request.POST.get(parameters[0]),data,parameters[0])}
				else:
					jsonresult = {"message":"Please, enter a correct parameter name"}
		else:
			jsonresult = {"message": "Please, enter only one parameter"}
		   
		return JSONResponse(jsonresult)
