#!/usr/bin/python2.7  
# -*- coding: utf-8 -*- 
from common import *
import os
import re
# data to transfer
dirfile="D:\project\lizheng\lizhengdata\数据\\"
dirfile=unicode(dirfile , "utf8")

#l=os.listdir(dirfile)
#print l
#f=open(dir+"filelist1.txt",'w')
#f.writelines(len(filelist1))
# st = filelist1.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0) 
class Updatedata(object):

	def __init__(self,dirfile):

		self.dir = dirfile#+"数据\\"
		#self.dir=unicode(self.dir , "utf8")
		self.n=[]
		
	def get_filelist(self,dir):
		self.filelist=os.listdir(self.dir)
		for self.file in self.filelist:
			self.p=re.compile('\d+')
			if not self.p.search(self.file):
				self.n.append(self.file)
		for self.x in self.n:
			self.filelist.remove(self.x)
		return self.filelist

	def print_filelist1(self,dir,filelist):
		f=open(self.dir+"filelist.txt",'w')
		f.write(str(len(self.filelist)))
		f.close

class Process(object):
	def __init__(self,file,dirfile):
		self.file=file
		self.dir=dirfile
	def get_date(self,file):
		self.p=re.compile(r'\d+')
		self.date=self.p.findall(self.file)
		self.date_new='%s-%s-%s:%s-%s-%s'%(self.date[0],self.date[1],self.date[2],self.date[3],self.date[4],self.date[5])
		return self.date_new
	def get_text(self,dir,file):

		self.f=open(self.dir+self.file,"r")
		self.rawdata=self.f.read()
		self.f.close
		return self.rawdata

	def get_transmitter(self,rawdata):
		self.p=re.compile(r'FYLZ\d+')
		self.transmitter=self.p.findall(self.rawdata)
		return self.transmitter
	def get_head(self,rawdata):
		self.d=re.compile(r'SM\n.*RS-232')
		self.head=self.d.findall(self.rawdata)
		return self.head
	def get_content(self,rawdata):
		self.c=re.compile(r'1\S+Eb90')
		self.content=self.c.findall(self.rawdata)
		return self.content

upload = Updatedata(dirfile)
filelist1=upload.get_filelist(dirfile)
upload.print_filelist1(dirfile,filelist1)

for file in filelist1:
	process=Process(file,dirfile)
	date=process.get_date(file) #get the date of receive message
	print date
	transmitter_list=process.get_transmitter(process.get_text(dirfile,file))#get the transmitter names
	head_list=process.get_head(process.get_text(dirfile,file))#get the head of the message
	content_list=process.get_content(process.get_text(dirfile,file))#get the content of the message
	lenth=len(transmitter_list)#get the transmitter number
	#process when head is null
	if len(head_list)<=lenth:
		j=0
		while j<=(lenth-len(head_list)):
			head_list.append("None")
			j+=1
	else:pass
	#process when content is null
	if len(content_list)<=lenth:
		j=0
		while j<=(lenth-len(content_list)):
			content_list.append("None")
			j+=1
	else:pass
	#puth the data to ckan
	j=0
	while j<lenth:
		data_temp=[]
		data_temp.append(head_list[j])
		data=[{
			"date":date,
			"transmitter":transmitter_list[j],
			"head":str(data_temp),
			"data":content_list[j],
			}]
		datastore_upsert(resource_id, data, api_key)
		j+=1 


			

	