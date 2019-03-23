import wget
import os
import requests
import json
from bs4 import BeautifulSoup

#FILE_PATH = "/Users/albertocm/Desktop/Ingeniería Telemática/TFG/TFG/EnisaFiles"
FILE_PATH = os.path.join(os.getcwd(),"EnisaFiles")
url = requests.get("https://www.enisa.europa.eu/topics/trainings-for-cybersecurity-specialists/online-training-material")
response = BeautifulSoup(url.content,"html.parser")
traininglinks = []
titles = []
resources = []
allinfo =[]
data = {}
data['resources'] = []
folder = FILE_PATH 
if not os.path.exists(folder):
    os.makedirs(folder)
# Obtiene todos los links de las diferentes clasificaciones de trainings
for link in response.findAll('tr'):
    if link.td.find('a') != None:
        traininglinks.append(link.td.a['href'])
# Conecta con cada uno de los links y obtiene los datos deseados.
for urltraining in traininglinks:
    page = requests.get(urltraining)
    print("CONECTANDO A: {0} ...".format(urltraining))
    responsetr = BeautifulSoup(page.content,"html.parser")
    for title in responsetr.find_all('h2'):
    	if title.text != None:
    		titles.append(title.text.replace("\u00a0"," "))

    for content in responsetr.find_all('table'):
        trg = ()
        if content.findAll('p') != None:
            contenttr = content.find_all('p')
            information = []
            for p in contenttr:
                information.append(p.text.replace("\u00a0"," "))
            resourcestr = content.find_all('a')
            for a in resourcestr:
                resources = []
                resources.append(a['href'])
            trg = (information, resources)
        allinfo.append(trg)

count = 0
for onetitle in titles:
    folder = FILE_PATH 
    folder = os.path.join(folder, onetitle)
    if not os.path.exists(folder):
        os.makedirs(folder)

    data['resources'].append({
        'source': 'Enisa',
        'title': onetitle,
        'target_audience': allinfo[count][0][0],
        'duration': allinfo[count][0][1],
        'description': allinfo[count][0][-1],
        'files': allinfo[count][0][2:-1]
        })
    

    with open('data.json', 'w') as outfile:
        json.dump(data,outfile, indent = 4)

    count+=1
    for dwnloadfile in allinfo[count][1]:
        dwnfile = wget.download(dwnloadfile, out = folder)
   
    

