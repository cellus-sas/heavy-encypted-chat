#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#require port 9999 free for localhost
#require specific NAT rule for allowing receiving   

#need ntp module
import os,sys
from telecom_operator.telecom_op import do_telecom_job  #telecom operator part
from crypto_client.run import do_key_regeneration_job #key regeneration part
from http_side.runkey import get_encrypted,get_decrypted #load encryption part
from http_side.run_server_conf import do_job_config #load encryption part
from http_side.run_server_remote_2_local import do_job_rem_2_loc #load encryption part
from http_side.run_server_local_2_remote import do_job_loc_2_rem #load encryption part
from gui.run_gui import do_job_rungui #load gui

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
	
	def load_param(self):
		#remote part
		try:
			with open('ip_remote','r') as f:
				ip_remote=f.read()
		except:
			print "no remote ip was given"
			ip_remote=""
		ip_obj=ip_remote.replace('\n','').replace(' ','').split(':')
		distant_ip=ip_obj[0]
		distant_port=int(ip_obj[1])

		#local part
		try:
			with open('ip_local','r') as f:
				ip_local=f.read()
			ip_obj=ip_local.replace('\n','').replace(' ','').split(':')
			local_ip=ip_obj[0]
			local_port=int(ip_obj[1])
		except:
			print "no local ip was given"
			ip_local=""

		#remote part
		try:
			with open('key_path','r') as f:
				key_path=f.read()
			key_path=key_path.replace('\n','').replace(' ','')
		except:
			print "no key path was given"
			key_path=""			
			
		return local_ip,local_port,distant_ip,distant_port,key_path
	
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
	
	def check_configuration_done(self):
		#print "checking if configuration is done ..."
		if os.path.exists('configuration_is_done'):
			ans=True
			os.remove('configuration_is_done')
		else:
			ans=False
		time.sleep(1)
		return ans
			
	def do_job(self):
		#need firewall rule if firewall exist
		#need router NAT port redirection rules  (rom outside port 10000 to localip port 10000  ) 
	
		#add randomizing local port
		#add reloading/changing local port
		#add https on both local and remote port access
		#add http user authentification for remote port acces

		#removing old trace
		#for each in self.file_2_clean:
		#	try:
		#		os.remove(each)
		#	except:
		#		pass
		self.ip_localhost="localhost"
		
		self.workable_situation=False
		
		print '#loading threadpool'
		self.pool_server = ThreadPool(7) #create pool
	
		print '>#run gui configuration receive thread PART 1/2 [preload]'
		waiting_configuration_is_done=False
		
		print ">#run thread server for configuration"
		try:
			os.remove('configuration_is_done')
		except:
			pass
		self.pool_server.add_task(do_job_rungui)
		
		self.pool_server.add_task(do_job_config,self.ip_localhost,9998)

		print '>#run thread for gui'

		
		print '>#run gui configuration receive thread PART 2/2 [wainting config]'
		#waiting result of configuration
		while not waiting_configuration_is_done:
			print "waiting configuration post..."
			waiting_configuration_is_done=self.check_configuration_done()
		#print self.load_param()
		print "Configuration receive"
		self.local_ip,self.local_port,self.distant_ip,self.distant_port,self.key_dir_path=self.load_param()
		print "start suite"

		print '>#run thread for synchonize passkey target in table'
		self.pool_server.add_task(do_key_regeneration_job,self.key_dir_path)

#		sys.exit()
		print '>#run thread server local>distant'
		self.pool_server.add_task(do_job_loc_2_rem,self.ip_localhost,9999)

		print '>#run thread server distant<local iplocal'+self.local_ip
		self.pool_server.add_task(do_job_rem_2_loc,self.local_ip,self.local_port)
	
		
		time.sleep(0.25)
		print '>#run thread telecom on '+self.distant_ip
		self.pool_server.add_task(do_telecom_job,self.local_ip,self.local_port,self.distant_ip,self.distant_port)
	

		
		self.pool_server.wait_completion()

	def __init__(self):
		self.file_2_clean=['current_key.pkl','ip_local','ip_remote','key_path','telecom_operator'+os.sep+'receiv.node','telecom_operator'+os.sep+'trans.node']		
		self.need_exit=False

#chaque tread mark son nom et son pid dans un obj

o=operator()
o.get_args()
o.do_job()
#do_job()
