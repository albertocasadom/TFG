import os
import shutil
import PyPDF2
import textract
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


DIR_PATH = os.getcwd()
dirlist = os.listdir(DIR_PATH)
if "EnisaFiles" in dirlist:
	DIR_PATH = os.path.join(DIR_PATH, "EnisaFiles")
	dirlist = os.listdir(DIR_PATH)
	print(dirlist)
	for folder in dirlist:
		FILE_PATH = os.path.join(DIR_PATH, folder)
		open("mainwordfile.txt","a").close()
		print(FILE_PATH)
		filelist = os.listdir(FILE_PATH)
		for file in filelist:
			if "pdf" in file:
				filename = os.path.join(FILE_PATH,file)
				#open allows you to read the file
				pdfFileObj = open(filename,'rb')
				#The pdfReader variable is a readable object that will be parsed
				pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
				#discerning the number of pages will allow us to parse through all #the pages
				num_pages = pdfReader.numPages
				count = 0
				text = ""
				#The while loop will read each page
				while count < num_pages:
				    pageObj = pdfReader.getPage(count)
				    count +=1
				    text += pageObj.extractText()
				#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
				if text != "":
				   text = text
				#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
				else:
				   text = textract.process(filename, method='tesseract', language='eng')
				# Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
				# Now, we will clean our text variable, and return it as a list of keywords.
				#The word_tokenize() function will break our text phrases into #individual words
				tokens = word_tokenize(text)
				#we'll create a new list which contains punctuation we wish to clean
				punctuations = ['(',')',';',':','[',']',',','/','.']
				#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
				stop_words = stopwords.words('english')
				#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
				keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

				with open("mainwordfile.txt","a") as file:
					for word in keywords:
						file.write(word)
						file.write(" ")
		if os.path.exists(os.path.join(FILE_PATH,"mainwordfile.txt")):
			os.remove(os.path.join(FILE_PATH,"mainwordfile.txt"))
		shutil.move("mainwordfile.txt",FILE_PATH)
DIR_PATH = os.getcwd()
dirlist = os.listdir(DIR_PATH)
if "SeedFiles" in dirlist:
	DIR_PATH = os.path.join(DIR_PATH, "SeedFiles")
	dirlist = os.listdir(DIR_PATH)
	print(dirlist)
	for folder in dirlist:
		FILE_PATH = os.path.join(DIR_PATH, folder)
		open("mainwordfile.txt","a").close()
		print(FILE_PATH)
		filelist = os.listdir(FILE_PATH)
		for file in filelist:
			if "pdf" in file:
				filename = os.path.join(FILE_PATH,file)
				#open allows you to read the file
				pdfFileObj = open(filename,'rb')
				#The pdfReader variable is a readable object that will be parsed
				pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
				#discerning the number of pages will allow us to parse through all #the pages
				num_pages = pdfReader.numPages
				count = 0
				text = ""
				#The while loop will read each page
				while count < num_pages:
				    pageObj = pdfReader.getPage(count)
				    count +=1
				    text += pageObj.extractText()
				#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
				if text != "":
				   text = text
				#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
				else:
				   text = textract.process(filename, method='tesseract', language='eng')
				# Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
				# Now, we will clean our text variable, and return it as a list of keywords.
				#The word_tokenize() function will break our text phrases into #individual words
				tokens = word_tokenize(text)
				#we'll create a new list which contains punctuation we wish to clean
				punctuations = ['(',')',';',':','[',']',',','/','.']
				#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
				stop_words = stopwords.words('english')
				#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
				keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

				with open("mainwordfile.txt","a") as file:
					for word in keywords:
						file.write(word)
						file.write(" ")
		if os.path.exists(os.path.join(FILE_PATH,"mainwordfile.txt")):
			os.remove(os.path.join(FILE_PATH,"mainwordfile.txt"))
		shutil.move("mainwordfile.txt",FILE_PATH)
				
'''
search = input("Type the word you want to find out: ")
repeat = 0
with open("pdfanalized.txt","r") as readfile:
	lines = readfile.readlines()
	for line in lines:
		words = line.split(' ')
		for w in words:
			if w.lower() == search.lower():
				print("La palabra {0} se repite ".format(search))
'''