import wget
import os
import requests
import json
import re
from bs4 import BeautifulSoup

#FILE_PATH = "/Users/albertocm/Desktop/Ingeniería Telemática/TFG/TFG/SeedFiles"
FILE_PATH = os.getcwd() + "/SeedFiles"
urlrsc = "http://www.cis.syr.edu/~wedu/seed/Labs_16.04/"
url = requests.get(urlrsc)
response = BeautifulSoup(url.content,"html.parser")
traininglinks = [] 
rsclinks = []
resources = []
dwnfiles = []
folder = FILE_PATH 
if not os.path.exists(folder):
	os.makedirs(folder)

with open("data.json",'r') as datafile:
			data = json.load(datafile)

for link in response.findAll("div",{"class":"one_third"}):
	traininglinks.append(link.a['href'])

for urltraining in traininglinks:
	urlres = urlrsc + urltraining
	url = requests.get(urlres)
	print("\nConnecting to: {0}".format(urlres))
	response = BeautifulSoup(url.content,"html.parser")
	for linkrsc in response.findAll('li'):
		if linkrsc.h3 != None:
			title = linkrsc.h3.text
			img = linkrsc.h3.img['src']
			diff = linkrsc.h3.get('class')
			if diff != None:
				diff = diff[0]
			else:
				diff = "Not defined"

			if "attack" in img:
				typetr = "attack"
			elif "exploration" in img:
				typetr = "exploration"
			else:
				typetr = "implementation"
		if linkrsc.p != None:
			description = linkrsc.p.text
		if urlrsc in linkrsc.a['href']:
			print("\nConnecting to: {0}".format(linkrsc.a['href']))
			urltr = requests.get(linkrsc.a['href'])
			root = linkrsc.a['href']
		elif "drive" in linkrsc.a['href']:
			pass
		elif ".pdf" in linkrsc.a['href'] or ".zip" in linkrsc.a['href']:
			pass
		else:
			urltr = urlres + linkrsc.a['href']
			root = urltr
			print("\nConnecting to: {0}".format(urltr))
			urltr = requests.get(urltr)

		response = BeautifulSoup(urltr.content,"html.parser")
		files = []
		dwnfiles = []
		information = []
		for li in response.findAll('li'):
			if li.a != None and "files/" in li.a['href']:
				files.append(li.a.text)
				dwnfiles.append(li.a['href'])
			elif li.a !=  None and ".py" in li.a['href']:
				files.append(li.a.text)
				dwnfiles.append(li.a['href'])

		rootlist = root.split('/')
		rootpath = root + rootlist[-2]
		rootpdf = rootpath + '.pdf'
		for dur in response.find(string = re.compile("week")):
			information.append(dur)		

		data['resources'].append({
			'source': 'SEEDLabs',
			'title': title,
			'type' : typetr,
			'difficulty': diff,
			'duration': information[0] + " week(s)",
			'description': description,
			'files': files
			})

		folder = FILE_PATH
		folder = os.path.join(folder,title.replace("/","-"))
		if not os.path.exists(folder):
			os.makedirs(folder)

		download = wget.download(rootpdf,out = folder)
		for file in dwnfiles:
			filepath= root + file
			if requests.get(filepath).status_code == 200:
				downloadfile = wget.download(filepath, out = folder)

with open("data.json",'w') as outfile:
	json.dump(data,outfile,indent = 4)
