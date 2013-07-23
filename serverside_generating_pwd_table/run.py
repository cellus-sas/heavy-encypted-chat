#!/usr/bin/env python
# -*- coding: UTF-8 -*-


#use it to generate key table between date1 et date2
import datetime,os,subprocess,shlex,time
import thread
import threading
 
from hashlib import md5
import pickle
from cStringIO import StringIO

ratio_integer_value=10 #crucial parameter : 1 mean one key per second #30 mean one key per 30 sec #60 mean one key per min (more you approach 1 more the keyfile obj is big)
ratio=float(float(1)/float(ratio_integer_value)) 

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


def checking_dirpath_content_lenght(path,content_len):
	if len(os.listdir(path))==content_len:
		return True
	else:
		return False

def wainting_to_make_obj(path,content_len,day_list_keyname):
	while checking_dirpath_content_lenght(path,content_len)==False:
		print "waiting all key for the day "+path
		time.sleep(1)
	print "ok ! "
	final_obj=[]
	for each_k in day_list_keyname:
		tempkey=""
		with open(path+os.sep+each_k[2]+'.pem','rb') as filekey:
			tempkey=filekey.read()
		tempkey=tempkey.replace('-----BEGIN RSA PRIVATE KEY-----\n','').replace('\n-----END RSA PRIVATE KEY-----\n','').replace('\n','')
		key_line=[each_k[0],each_k[1],tempkey]
		final_obj.append(key_line)
		
	#run thread wainting that all day are ziped to zip-it
	output = open("data"+os.sep+part_a+'.pkl', 'wb')
	pickle.dump(final_obj, output, -1)
	output.close()	

def runnowait(mycommand):
   args=shlex.split(mycommand)
   p=subprocess.Popen(args)

d = datetime.datetime.strptime('22 Jul 2013', '%d %b %Y')
e = datetime.datetime.strptime('24 Jul 2013', '%d %b %Y')
delta = datetime.timedelta(days=1)

path="data"
try:
	os.mkdir(path)
except:
	pass

cp_t=0
th_l=[]
while d <= e:
    day_table=[]
    day_list_keyname=[]
    part_a = d.strftime("%y%m%d")
    try:
		os.mkdir(path+os.sep+part_a)
    except:
		pass
    for i in range(0,int(86400*ratio)):
		print "Generating "+str(i)
		part_b = str(int(i*(1/ratio))).zfill(5)
		day_table.append([part_a,part_b,[]])
		#multithread add generate key for this
		keyname=md5(part_a+part_b).hexdigest()
		day_list_keyname.append([part_a,part_b,keyname])
		filename=path+os.sep+part_a+os.sep+keyname+'.pem'
		try:
			with open(filename): pass
		except IOError:
			#print 'Oh dear.'
			runnowait('openssl genrsa -out '+filename+' 2048')
			pass
			
    #print checking_dirpath_content_lenght()
    th_l.append(FuncThread(wainting_to_make_obj, path+os.sep+part_a,len(day_list_keyname),day_list_keyname))
    th_l[cp_t].start()

    d += delta
    cp_t=cp_t+1

print "exit"
for i in range(0,len(th_l)):
	th_l[i].join()
print "ending"
	


