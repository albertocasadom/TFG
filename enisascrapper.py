import wget
import os
import requests
import json
from bs4 import BeautifulSoup

FILE_PATH = "/home/hacklberto/Telematics Degree/TFG/TFG/EnisaFiles"
url = requests.get("https://www.enisa.europa.eu/topics/trainings-for-cybersecurity-specialists/online-training-material")
response = BeautifulSoup(url.content,"html.parser");
traininglinks = []
informationdivided = []
titles = []
numelemp = 0
resources = []
allinfo =[]
data = {}
data['resources'] = []

# Obtiene todos los links de las diferentes clasificaciones de trainings
for link in response.findAll('tr'):
    if link.td.find('a') != None:
        traininglinks.append(link.td.a['href'])
# Conecta con cada uno de los links y obtiene los datos deseados.
for urltraining in traininglinks:
    page = requests.get(urltraining)
   # print(f"CONECTANDO A: {urltraining} ...")
    responsetr = BeautifulSoup(page.content,"html.parser")
    for title in responsetr.find_all('h2'):
    	if title.text != None:
    		titles.append(title.text)
    		print(title.text)

    for content in responsetr.find_all('table'):
        if content.findAll('p') != None:
            contenttr = content.find_all('p')
            information = []
            for p in contenttr:
                information.append(p.text)
            informationdivided.append(information)
            resourcestr = content.find_all('a')
            for a in resourcestr:
                resources.append(a['href'])
count = 0

for onetitle in titles:   
    data['resources'].append({
        'resource':{
        'source': 'enisa',
        'title': onetitle,
        'target_audience': informationdivided[count][0],
        'duration': informationdivided[count][1],
        'description': informationdivided[count][-1],
        'files': informationdivided[count][2:-1]}
        })
    count+=1

with open('data.json', 'w') as outfile:
    json.dump(data,outfile)


folder = FILE_PATH 

if not os.path.exists(folder):
    os.makedirs(folder)

for rsrc in resources:
    download = wget.download(rsrc, out = folder)
    