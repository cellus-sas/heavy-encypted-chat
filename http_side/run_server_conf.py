#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import SocketServer,sys,os,socket
import urllib2,urllib
import runkey
import random
import pickle
import runkey

local=False
random_port=False #debug 9999
#print ('#handle request from local client in order to encrypt the data then send to remote host')

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def data_treatment(self,clear_text=""):
		global local

		if local==True:
			path_trans_node=os.getcwd()+os.sep+".."+os.sep+"telecom_operator/trans.node"
			base_dir=os.getcwd()+os.sep+".."+os.sep
		else:
			path_trans_node=os.getcwd()+os.sep+"telecom_operator/trans.node"
			base_dir=os.getcwd()+os.sep
	
		in_str= urllib.unquote(clear_text)
		print in_str
		
		#localip~~~localport~~~distantip~~~distantport~~~keypath
		e=in_str.split('~~~')
		la=e[0] #local ip
		lp=e[1] #local port
		ra=e[2] #remote ip
		rp=e[3] #remote port
		kp=e[4] #key path		
		fla=la+':'+lp
		fra=ra+':'+rp
		print la,":",lp
		print ra,":",rp
		print "path ",kp
		print "base dir "+base_dir

		print kp

		#remote part
		try:
			with open(base_dir+'ip_remote','w') as f:
				f.write(fra)
		except:
			print "no remote ip was given"
			ip_remote=""

		#local part
		try:
			with open(base_dir+'ip_local','w') as f:
				f.write(fla)
		except:
			print "no local ip was given"
			ip_local=""

		#remote part
		try:
			with open(base_dir+'key_path','w') as f:
				key_path=f.write(kp)
		except:
			print "no key path was given"
			key_path=""	

		#said that configuration is done to main thread
		with open('configuration_is_done','w') as f:
			f.write('')


    def handle(self):
		#print os.getcwd()
		try:
			with open(os.getcwd()+os.sep+'http_side'+os.sep+'exit_local_2_remote','r') as f:
				f.read()
			sys.exit()
		except:
			pass
		#print "handel"
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		#print "{} wrote:".format(self.client_address[0])
		try:
			required_field= self.data.split('GET /?&data=')[1]
			print required_field
			# just send back the same data, but upper-cased
		except:
			print "required_field error self.data='"+ self.data+"'"
			pass
		#try:
		self.data_treatment(clear_text=required_field)
		#except:
		#	print "data is incorrect need to be http://host:port/?&data="
		#	pass
		#self.request.sendall(self.data.upper())
	

def getmylocaladdress():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		ans= s.getsockname()[0]
		s.close()	
	except:
		print "error to get local address"
		ans=""
		pass
	return ans
	
def setlocaladdress():
	global local
	ip=getmylocaladdress()
	if local==True:
		base_dir=os.getcwd()+os.sep+".."+os.sep
	else:
		base_dir=os.getcwd()+os.sep
	if ip!="":
		try:
			with open(base_dir+os.sep+'gui'+os.sep+"ressource"+os.sep+"ajax"+os.sep+"localip.json",'w') as f:
				f.write('{\n"local_adress": "'+ip+'"\n}')
		except:
			print "error during writing local adress to json"
			pass
def do_job_config(HOST="localhost",PORT=9998):
	global random_port
	##print host
		
	setlocaladdress()
	
	if random_port==True:
		PORT=random.randint(8000,12000)
		#print "random port is "+str(PORT)
	# Create the server, binding to localhost on port 9999
	SocketServer.TCPServer.allow_reuse_address = True
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
if __name__ == "__main__":
	#print "need be run "
	do_job_config()
