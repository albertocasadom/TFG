import wget
import os
import requests
import json
import re
from bs4 import BeautifulSoup

FILE_PATH = "/home/hacklberto/Telematics Degree/TFG/TFG/SeedFiles"
urlrsc = "http://www.cis.syr.edu/~wedu/seed/Labs_16.04/"
url = requests.get(urlrsc)
response = BeautifulSoup(url.content,"html.parser")
traininglinks = [] 
rsclinks = []
data = {}
data['resources'] = []
information = []
resources = []
folder = FILE_PATH 
if not os.path.exists(folder):
	os.makedirs(folder)

for link in response.findAll("div",{"class":"one_third"}):
	traininglinks.append(link.a['href'])

for urltraining in traininglinks:
	urlres = urlrsc + urltraining
	url = requests.get(urlres)
	response = BeautifulSoup(url.content,"html.parser")
	for linkrsc in response.findAll('li'):
		if linkrsc.h3 != None:
			title = linkrsc.h3.text
		if linkrsc.p != None:
			description = linkrsc.p.text
		if urlrsc in linkrsc.a['href']:
			urltr = requests.get(linkrsc.a['href'])
			root = linkrsc.a['href']
		elif "drive" in linkrsc.a['href']:
			continue
		elif ".pdf" in linkrsc.a['href'] or ".zip" in linkrsc.a['href']:
			continue
		else:
			urltr = urlres + linkrsc.a['href']
			root = urltr
			urltr = requests.get(urltr)
		response = BeautifulSoup(urltr.content,"html.parser")	
		rootlist = root.split('/')
		root = root + rootlist[-2] + '.pdf'
		print(root)
		download = wget.download(root,out =folder)
    	data['resources'].append({
			'resource':{
				'source':'SEEDLabs',
				'title': title,
				'target_audience': 'Students',
				'description': description,
				'Enunciado': root
			}
		})
    	with open('data.json','w+') as outfile:
    		json.dump(data,outfile, indent = 4)