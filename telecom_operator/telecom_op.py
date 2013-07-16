#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#test l'adresse distante de differente maniere pr verifier qu'elle est joignable


import urllib2,time,urllib
import os
from hashlib import md5
import pickle
import base64


def log(arg):
	try:
		with open('log.txt','r') as l:
			pass
	except:
		with open('log.txt','w') as l:
			l.write('')
	with open('log.txt','a') as l:
		l.write('\n'+str(arg))

local=False

class telecom(object):
	def set_var(self):
		self.max_chat_json_element=5
		self.show_what_we_send=True
		
		
		self.delay_wait_main=0.1 #second
		self.delay_checking_when_host_if_online=0.5 #second
		self.delay_checking_when_host_if_offline=5 #second
		
		self.local=True
		if self.local==True:
			self.transmit_nodefile=os.getcwd()+os.sep+'trans.node'
			self.receive_nodefile=os.getcwd()+os.sep+'receiv.node'
		else:
			self.transmit_nodefile=os.getcwd()+os.sep+'telecom_operator'+os.sep+'trans.node'
			self.receive_nodefile=os.getcwd()+os.sep+'telecom_operator'+os.sep+'receiv.node'
		print "transmit "+self.transmit_nodefile
		print "receiv "+self.receive_nodefile
		
				
		self.howmanytime_before_recheck_if_online=25 # mean that it is relative to self.delay_checking_when_host_if_online
		
		self.testing_host=self.distant_ip+":"+str(self.distant_port)
		self.testing_adress='http://'+self.testing_host
		
		self.local_adress='http://'+self.local_ip+':'+str(self.local_port)		
		self.checkingwhenalive_count=0
		self.is_alive=False

		self.real_transmit=[]
		self.real_reveive=[]
		


	def remotehostisalive(self):
		#ajouter un timeout au cas ou ca repond pas
		try:
			c=urllib2.urlopen(self.testing_adress).read()
		
			if str(c).upper().find("HOST: "+self.testing_host.upper())>-1:
				self.is_alive=True
				return True
			else:
				self.is_alive=False
				return False
		except:
			return False
			pass
			
	def define_state(self):
		if self.is_alive==True:
			self.remote_is_online()
		else:
			self.remote_is_offline()

	def update_state(self):
		self.remotehostisalive()
		self.define_state()
		
	def __init__(self,local_ip,local_port,distant_ip,distant_port):
		print "init telecom"
		#init var
		self.distant_ip=distant_ip
		self.distant_port=distant_port
		self.local_ip=local_ip
		self.local_port=local_port #assuming local_ip is localhost
		self.set_var()
		#init state
		self.update_state()

	def remote_is_offline(self):
		print "remote_is_offline"
		#on attend
		self.remotehostisalive()
		if self.is_alive==True:
			#reup connection
			time.sleep(self.delay_checking_when_host_if_offline)
			pass
		else:
			#ouvrir l ecoute pr le changement de destinataire (o k ou l ip distant à changer)
			time.sleep(self.delay_checking_when_host_if_offline)
		#on verifi si connecter
		self.main_telecom_loop()		
		pass
		
	def remote_is_online(self):
		#print "remote_is_online"
		time.sleep(self.delay_checking_when_host_if_online)
		#verification relative to online
		#main_telecom_loop
		#
		#une fois sur n verifier que l host est en vie
		self.main_telecom_loop()		
		pass

	def incrementalive_count(self):
		self.checkingwhenalive_count=self.checkingwhenalive_count+1
		if self.checkingwhenalive_count>=self.howmanytime_before_recheck_if_online:
			print "recheck alive connectivity"
			self.checkingwhenalive_count=0
			self.remotehostisalive()
					

			
	def do_transmit(self):
		global local
		if local==True:
			path_trans_node=os.getcwd()+os.sep+".."+os.sep+"telecom_operator/trans.node"
		else:
			path_trans_node=os.getcwd()+os.sep+"telecom_operator/trans.node"

		#get hash of file to check integrity before write
		try:
			with open(path_trans_node,'r') as p:
				start_h=md5(p.read()).digest()
		except:
			start_h=""
			pass

		try:
			pkl_file = open(path_trans_node, 'rb')
			trans_node_obj = pickle.load(pkl_file)
		except:
			trans_node_obj=[]
		#print "do transmission"
		
		if len(trans_node_obj)>0:
			#on peu verifier que l host est vivant
			#print "entering transmission procedure"
			forged_url=self.testing_adress
			#print trans_node_obj
			for i in range(0,len(trans_node_obj)):
				is_send=False
				#integrate iv in d or h parameter
				#verifier la longeur si probleme coupé en plusieur requettes
				try:
					element_to_send = trans_node_obj[i]
					e=base64.b64encode(element_to_send[0])
					h= base64.b64encode(element_to_send[1])
					d= str(element_to_send[2])+"-"+element_to_send[3]+"-"+element_to_send[4]
					#enctext,iv,d,h,ts
					url_2_send=self.testing_adress+"/?&enc_text="+e+"&h="+h+"&d="+d #distant url
					url_2_send_feedback=self.local_adress+"/?&enc_text="+e+"&h="+h+"&d="+d #distant url
					
					print "url2send> "+ url_2_send
					#print "url2send_feedback> "+ url_2_send_feedback

					sr=urllib2.urlopen(url_2_send).read()
					is_send=True
#---------------------------------------------------------------------------------------------------------------- on work >
					if self.show_what_we_send==True: 
						try:
							srf=urllib2.urlopen(url_2_send_feedback).read()
							is_send_feedback=True
						except:
							is_send_feedback=True
#---------------------------------------------------------------------------------------------------------------- on work <		
				except:
					sr=""
					is_send=False
				
				if is_send==True:
					#print "message send (popit from send obj)"
					trans_node_obj.pop(i)
					i=i-1	
					
					
			file_has_change=True
			#check if no change has occured with h
			try:
				with open(path_trans_node,'r') as p:
					end_h=md5(p.read()).digest()
			except:
				end_h=""
				pass
			if start_h==end_h:
				file_has_change=False
			if file_has_change==True:
				#procedure if change has occured
				pass
			else:				
				output = open(path_trans_node, 'wb')
				pickle.dump(trans_node_obj, output, -1)
				output.close()	
					
				
	def do_receive(self):
		global local
		#print "do receive from"
		#print os.getcwd()
		if local==True:
			path_receiv_node=os.getcwd()+os.sep+".."+os.sep+"telecom_operator/receiv.node"
		else:
			path_receiv_node=os.getcwd()+os.sep+"telecom_operator/receiv.node"

		#print "do receive path receive"
		#print path_receiv_node

		#get hash of file to check integrity before write
		try:
			with open(path_receiv_node,'r') as p:
				start_h=md5(p.read()).digest()
		except:
			start_h=""
			pass

		try:
			pkl_file = open(path_receiv_node, 'rb')
			receiv_node_obj = pickle.load(pkl_file)
		except:
			sys.exit()
			receiv_node_obj=[]
		#print "do receive"
		file_has_change=True
		#print receiv_node_obj
		if len(receiv_node_obj)>0:
			#on peu verifier que l host est vivant
			#print "entering receive procedure"
			for i in range(0,len( receiv_node_obj)):
				is_receiv=False
				#integrate iv in d or h parameter
				try:
#					c=update_json
					element_to_receive = receiv_node_obj[i]
					#update json for chat
					if local==True:
						#print "dir modified for json"
						#print os.getcwd()
						json_path=os.getcwd()+os.sep+".."+os.sep+"pyqt_app_gui"+os.sep+"ressource"+os.sep+"ajax"+os.sep+"current.json"
					else:
						#print "not modified for json"
						json_path=os.getcwd()+os.sep+"pyqt_app_gui"+os.sep+"ressource"+os.sep+"ajax"+os.sep+"current.json"
					#print "json path > "+json_path
					#print "need to add this to json"
					with open(json_path,'r') as json_f:
						jsc=json_f.read()
					tj=	jsc.split('"],\n')
					middle_json=tj[-1]

					#print receiv_node_obj
					pre_json=tj[:len(tj)-1]
					if len(pre_json)>=self.max_chat_json_element:
						pre_json=pre_json[(len(pre_json)-self.max_chat_json_element):len(pre_json)]
						pre_json[0]="{\n"+pre_json[0]

					last=middle_json.split('"]\n')[0]
					pre_json.append(last)
					lastnum=int(last.split('":')[0].replace('"',''))
					#print element_to_receive[0]#<- --------------------------gerer les plus et les probleme d encodage en dessous
					if element_to_receive[2]==str(self.local_ip):
						element_to_receive[2]="me"
					element_to_receive[0]=element_to_receive[0].replace('+',' ')
					new_elem='"'+str(lastnum+1)+'": ["'+element_to_receive[0].replace('"','\\"')+'","'+element_to_receive[2]+'","'+element_to_receive[1]
					##print "new elem"+str(new_elem)
					new_elem=new_elem
					#print  "new elem not in prejson" +str(new_elem not in pre_json)
					#print "pre_json> "+str(pre_json)
					#~ if (new_elem not in pre_json)==True:
						#~ pre_json.append(new_elem)
					
					new_json_code= '"],\n'.join(pre_json)+'"],\n'+new_elem+'"]\n}'		
					with open(json_path,'w') as json_f:
						json_f.write(new_json_code)
					is_receiv=True
				except:
					is_receiv=False
				if is_receiv==True:
					receiv_node_obj.pop(i)
					i=i-1

			
			#check if no change has occured with h
			try:
				with open(path_receiv_node,'r') as p:
					end_h=md5(p.read()).digest()
			except:
				end_h=""
				pass
			if start_h==end_h:
				file_has_change=False
			if file_has_change==True:
				#procedure if change has occured
				pass
			else:				
				output = open(path_receiv_node, 'wb')
				pickle.dump(receiv_node_obj, output, -1)
				output.close()	

	def main_telecom_loop(self):
		##print "main loop"
		self.delay_wait_main=0.1 #second
		if self.is_alive==True:
			#print "main loop with alive host"
			self.incrementalive_count()
			self.do_receive() #threaded
			self.do_transmit() #threaded
		else:
			#print "waiting remote"
			pass
		time.sleep(self.delay_wait_main)
		pass
	
def do_telecom_job(local_ip,local_port,distant_ip,distant_port):	
	global local
	#print "do_telecom_job"
	t=telecom(local_ip,local_port,distant_ip,distant_port)
	#print "do_telecom_job ok"
	while 1:
		t.define_state()
	
	
	
if __name__ == "__main__":
	local=True
	#print "need be run "
	do_telecom_job(local_ip="192.168.1.44",local_port=10000,distant_ip="192.168.1.25",distant_port=10000)

