from django.shortcuts import render
from django.template import loader
from django.shortcuts import render_to_response
import speech_recognition as sr
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from collections import defaultdict
from heapq import nlargest
from string import punctuation
from nltk.tokenize import sent_tokenize,word_tokenize
import pyaudio,os,sys,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email import encoders
import zipfile
from email.mime.base import MIMEBase
import csv
import time
import pyttsx3
rec=None
orginalList=[]
sumofsum=[]
tstart=[]
tend=[]
tdiffer=[]
sumcomp=[]
numlines=[]

List=[]

dList=[]
bList=[]
eList=[]
disp=""
myval=""
mincut=0.1
maxcut=0.9
compList=[]
sList=[]
uniquewords=set()
stopwords=set(stopwords.words('english')+list(punctuation))
conjunction=["for","and","nor","but","or","yet","so"]
question=["am","was","which","what","whose","who","whom","where","when","how","why","are","can","is","do","did","does","have","could","shall","should","may","whether","whatsoever","had","will"]
def help(request):
	return render(request,"help.html",{})
def hello(request):
	return render(request,"index.html",{})
@csrf_exempt
@requires_csrf_token

def call(request):
	return render(request,"dot.html",{})
	#return HttpResponse("your respones")
def cool(request):
	r = sr.Recognizer()
	with sr.Microphone() as source:

		audio = r.listen(source)
		try:
			rec=r.recognize_google(audio)
			List.append(rec)
		except Exception as e:
			pass
		return render(request,"index.html",{'context':List})
@csrf_exempt
@requires_csrf_token
def simple(request):
	rec=""
	r=sr.Recognizer()
	with sr.Microphone() as source:
		audio=r.listen(source)
		try:
			rec=r.recognize_google(audio)
			# Done=word_tokenize(rec)
			# print ("the value of the done:",Done)
			# if "content" in Done:
			# 	rec="content"
			# elif "meaning" in Done:
			# 	rec="meaning"
			# elif rec=="exit exit":
			# 	rec="stop"
		except Exception as e:
			pass
		#print("the value of the rec is:",rec)
		return HttpResponse(rec)
def meaning(msg):

	newfi=open('/home/godalone/Pythonre/done/webmeaning','a')
	newfi.truncate(0)
	newfi=open('/home/godalone/Pythonre/done/webmeaning','a')

	result=word_tokenize(msg)
	for i in result:
		if i not in stopwords:

			word=wn.synsets(i)
			w1="\n"+word[0].name()+"\n"
			w2=word[0].lemmas()[0].name()+"\n"
			w3=word[0].definition()+"\n"
			w4=str(word[0].examples())


			newfi.write(w1)
			newfi.write(w2)
			newfi.write(w3)
			newfi.write(w4)
			newfi.write("\n_______________________________________________________________________________________________________________________\n")
	newfi.close()
def compute_frequencies(word_sent):
	freq=defaultdict(int)
	for s in word_sent:
		for word in s:
			if word not in stopwords:
				freq[word] += 1
	m=float(max(freq.values()))
	for w in list(freq):
		freq[w]=freq[w]/m
		if freq[w] >= maxcut or freq[w] <= mincut:
			del freq[w]
	return freq




def summarize(text,n):
	sents=sent_tokenize(text)
	if n > len(sents):
		return " "
	word_sent=[word_tokenize(s.lower()) for s in sents]
	freq=compute_frequencies(word_sent)
	ranking=defaultdict(int)
	for i,sent in enumerate(word_sent):
		for w in sent:
			if w in freq:
				ranking[i] += freq[w]

	sents_idx=rank(ranking,n)
	return [sents[j] for j in sents_idx]
def rank(ranking,n):
	return nlargest(n,ranking,key=ranking.get)


def callme(sentmsg):
	global disp
	global myval
	try:
		user=sentmsg
		user=user.lower()
		res=word_tokenize(user)
		lastword=res[-1:]
		for i in lastword:
			if i=="you":
				tmp='n'
			else:
				tmp=wn.synsets(i)[0].pos()
		if res[0] in question and (tmp=='n' or tmp=='a'):
			if disp != "":
				user=" . "+user+" ?"
			else:
				user=" "+user+" ? "

			myval=myval+user+" "
		elif(tmp == 'n' or tmp=='a') and (user !="exit exit"):
			if disp=="":
				disp=disp+" ."
				myval=myval+user+" "
				
			elif res[0] in conjunction:
				myval=myval+" "+user+" "
				user=" "+user
			else:
				newdisp=disp+" "+user+" . "
				user=newdisp
				myval=myval+newdisp
				disp=""

		else:
			if disp != "" and user !="exit exit":
				user=". "+user
				myval=myval+user
				disp=""
			elif user !="exit exit":
				user=user+" "
				myval=myval+user
		if user == "clear file":
			fil=open('/home/godalone/Pythonre/done/webspoke','a')
			fil.truncate(0)
			webmean=open('/home/godalone/Pythonre/done/webmeaning','a')
			websum=open('/home/godalone/Pythonre/done/websummarize','a')
			webmean.truncate(0)
			websum.truncate(0)
			fil.close()
			websum.close()
			webmean.close()

			
		elif user=="exit exit":
			disp=""
			return "stop"
		return user
	except Exception as e:
		return "error"
	return user

@csrf_exempt
def fileclear(request):
	fil=open('/home/godalone/Pythonre/done/webspoke','a')
	webmean=open('/home/godalone/Pythonre/done/webmeaning','a')
	websum=open('/home/godalone/Pythonre/done/websummarize','a')
	fil.truncate(0)
	webmean.truncate(0)
	websum.truncate(0)
	fil.close()
	webmean.close()
	websum.close()
	return HttpResponse("success")
			



@csrf_exempt
def fullcore(request):
	global sList
	global bList
	global eList

	rec=""
	r=sr.Recognizer()
	then=time.time()
	with sr.Microphone() as source:
		try:
			audio=r.listen(source)
			sendmsg=r.recognize_google(audio)

			rec=callme(sendmsg)
			sList.append(rec)
			now=time.time()
			bList.append(then)
			eList.append(now)

		except Exception as e:
			pass

		return HttpResponse(rec)
@csrf_exempt
def filecsv(request):
	global bList
	global eList
	global dList
	global compList
	global sList
	llen=len(sList)
	for i in range(llen):
		print("heoo")
		can=eList[i]-bList[i]
		dList.append(can)
	for j in range(llen):
		tmpList=[]
		tmpList.append(sList[j])
		tmpList.append(bList[j])
		tmpList.append(eList[j])
		tmpList.append(dList[j])
		compList.append(tmpList)
	with open('/home/godalone/Pythonre/done/mydataset','a') as f:
		w=csv.writer(f)
		w.writerows(compList)
	sList[:]=[]
	bList[:]=[]
	eList[:]=[]
	dList[:]=[]
	compList[:]=[]
	return HttpResponse("")

@csrf_exempt
def sumfile(request):
	global tdiffer
	global sumcomp
	global orginalList
	global sumofsum
	global tstart
	global tend
	global numlines
	llen=len(tstart)
	for i in range(llen):
		can=tend[i]-tstart[i]
		tdiffer.append(can)
	for j in range(llen):
		tmpList=[]
		tmpList.append(orginalList[j])
		tmpList.append(numlines[j])
		tmpList.append(sumofsum)
		tmpList.append(tstart[j])
		tmpList.append(tend[j])
		tmpList.append(tdiffer[j])
		sumcomp.append(tmpList)
	with open('/home/godalone/Pythonre/done/summarizeddataset','a') as f:
		w=csv.writer(f)
		w.writerows(sumcomp)
	orginalList[:]=[]
	sumofsum[:]=[]
	tstart[:]=[]
	tend[:]=[]
	numlines[:]=[]
	tdiffer[:]=[]
	sumcomp[:]=[]

	return HttpResponse("")
@csrf_exempt
def fmean(request):
	global myval

	try:

		newfile=open("/home/godalone/Pythonre/done/webspoke",'a')
		myval=" "+myval
		newfile.write(myval)
		newfile.close()
		with open('/home/godalone/Pythonre/done/webspoke') as file:
			mydata=file.read()
		myval=""
	except Exception as e:
		pass
	return HttpResponse(mydata)

@csrf_exempt
def fcont(request):
	with open('/home/godalone/Pythonre/done/webspoke') as f:
		Fcontentfile=f.read()
	meaning(Fcontentfile)
	with open('/home/godalone/Pythonre/done/webmeaning') as k:
		fileret=k.read()
	return HttpResponse(fileret)

@csrf_exempt
def ssum(request):
	global orginalList
	global sumofsum
	global tstart
	global tend
	global numlines
	
	can=int(request.POST['vval'])
	numlines.append(can)
	with open('/home/godalone/Pythonre/done/webspoke') as infile:
		Ffile=infile.read()
	orginalList.append(Ffile)
	Summer=open('/home/godalone/Pythonre/done/websummarize','a')
	stime=time.time()
	tstart.append(stime)
	s=summarize(Ffile,can)
	etime=time.time()
	tend.append(etime)
	for k in s:
		sumofsum.append(k)

		k="\n#)"+k+"\n"
		Summer.write(k)
	Summer.write("\n_______________________________________________________________________________________________________________________\n")
	Summer.close()

	with open('/home/godalone/Pythonre/done/websummarize') as fi:
		Finalresult=fi.read()
	return HttpResponse(Finalresult)

@csrf_exempt
def t2speech(request):
	engine=pyttsx3.init()
	with open('/home/godalone/Pythonre/done/webspoke') as f:
		kk=f.read()
	engine.say(kk)
	engine.setProperty('rate',60)
	engine.setProperty('volume',0.9)
	engine.runAndWait()
	return HttpResponse("")

@csrf_exempt
def smail(request):
	jname=request.POST['fname']
	jmail=request.POST['fmail']

	zf=zipfile.ZipFile("/home/godalone/Pythonre/Content","w")
	for dirname, subdirs, files in os.walk("/home/godalone/Pythonre/done"):
		zf.write(dirname)
		for f in files:
			zf.write(os.path.join(dirname,f))
	zf.close()
	try:
		msg = MIMEMultipart()
		msg['From'] = "vinarasu77@gmail.com"
		msg['To'] = jmail
		msg['Subject'] = "speech_recognition & Text Summarization"
		msg.attach(MIMEText("Hello dear "+jname))
		mssg=MIMEBase('application','zip')
		mssg.set_payload(open('/home/godalone/Pythonre/Content','rb').read())
		encoders.encode_base64(mssg)
		mssg.add_header('Content-Disposition','attachment',filename=jname+'.zip')
		msg.attach(mssg)
		server = smtplib.SMTP('smtp.gmail.com: 587')

		server.starttls()

		# Login Credentials for sending the mail
		server.login('vinarasu77@gmail.com', '@soniya@1999')


		# send the message via the server.
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()
		result=1

	except Exception as e:
		result=0

	return HttpResponse(result)

