import wget
import os
import requests
from bs4 import BeautifulSoup

FILE_PATH = "/home/hacklberto/Telematics Degree/TFG/TFG/SeedFiles"
urlrsc = "http://www.cis.syr.edu/~wedu/seed/Labs_16.04/"
url = requests.get(urlrsc)
response = BeautifulSoup(url.content,"html.parser")
traininglinks = [] 
rsclinks = []
for link in response.findAll("div",{"class":"one_third"}):
	traininglinks.append(link.a['href'])

for urltraining in traininglinks:
	urlres = urlrsc + urltraining
	url = requests.get(urlres)
	response = BeautifulSoup(url.content,"html.parser")
	for linkrsc in response.findAll('li'):

		if urlrsc in linkrsc.a['href']:
			urltr = requests.get(linkrsc.a['href'])
		else:
			urltr = urlres + linkrsc.a['href']
			print(urltr)
			urltr = requests.get(urltr)

		response = BeautifulSoup(urltr.content,"html.parser")
		title = response.div.div.h1.text
		response.findAll()