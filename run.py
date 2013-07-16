#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#need ntp
import sys
from telecom_operator.telecom_op import do_telecom_job  #telecom operator part
from crypto_client.run import do_key_regeneration_job #key regeneration part
from http_side.runkey import get_encrypted,get_decrypted #load encryption part
from http_side.run_server_remote_2_local import do_job_rem_2_loc #load encryption part
from http_side.run_server_local_2_remote import do_job_loc_2_rem #load encryption part
#from pyqt_app_gui.webbrowser import start_ui #load ui part

from Queue import Queue
from threading import Thread



#todo function pour cree les fichier qui font quitter tout les thread
#lancer cette funciton qd on ferme le gui

#todo ajout get key info of timestamp #pour le cas ou
#todo action dans do_job_rem_2_loc and do_job_loc_2_rem pour que les requete aboutisse à la regeneration du json ou à l'envoi de la requete pour pusher les info vers


import time

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()
            
class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
        
class operator(object):
	

	def clean_out(self):
		global file_2_clean
		os.remove()
	
	def wait_delay(self,d,string_info):
		print string_info
		print 'sleeping for (%d)sec' % d
		time.sleep(d)
		print "end sleep"
	
	def load_ip(self):
		try:
			with open('ip_remote','r') as f:
				ip_remote=f.read()
		except:
			ip_remote=""
		ip_obj=ip_remote.replace('\n','').replace(' ','').split(':')
		distant_ip=ip_obj[0]
		distant_port=int(ip_obj[1])
		try:
			with open('ip_local','r') as f:
				ip_local=f.read()
			ip_obj=ip_local.replace('\n','').replace(' ','').split(':')
			local_ip=ip_obj[0]
			local_port=int(ip_obj[1])
		except:
			ip_local=""
		return local_ip,local_port,distant_ip,distant_port
	
	def get_args(self):
		try:
			[n,l,r,d]=sys.argv[:4]
			print l,r,d
		except:
			print "Arg is: (1)localip:port (2)remoteip:port (3)dirofkey"
			pass
		try:
			[n,r,d]=sys.argv[:4]
			#need specify ip if more than one device exist and addreses
			
			print l,r,d
		except:
			print "Arg is: (1)remoteip:port (3)dirofkey"
			pass
	
			
			
	def do_job(self):
		#need firewall rule if firewall exist
		#need router NAT port redirection rules  (rom outside port 10000 to localip port 10000  ) 
	
		#add randomizing local port
		#add reloading/changing local port
		#add https on both local and remote port access
		#add http user authentification for remote port acces
		
	
		self.ip_localhost="localhost"
		self.local_ip,self.local_port,self.distant_ip,self.distant_port=self.load_ip()
		self.key_dir_path="/home/noname/Desktop/Integrate_chat/crypto_client/key/"
		
		self.workable_situation=False
		self.pool_server = ThreadPool(5)
	
		print '#run thread server local>distant'
		self.pool_server.add_task(do_job_loc_2_rem,self.ip_localhost,9999)
	
		print '#run thread server distant<local iplocal'+self.local_ip
		self.pool_server.add_task(do_job_rem_2_loc,self.local_ip,self.local_port)
	
		print '#run thread for synchonize passkey target in table'
		self.pool_server.add_task(do_key_regeneration_job,self.key_dir_path)
		
		time.sleep(0.25)
		print '#run thread telecom on '+self.distant_ip
		self.pool_server.add_task(do_telecom_job,self.local_ip,self.local_port,self.distant_ip,self.distant_port)
	
		#print '#run thread for gui'
		#pool_server.add_task(start_ui)
		#need to open file html
		
		self.pool_server.wait_completion()

	def __init__(self):
		self.file_2_clean=['current_key.pkl','ip_remote','ip_local']
		self.need_exit=False

#chaque tread mark son nom et son pid dans un obj

o=operator()
o.get_args()
o.do_job()
#do_job()
