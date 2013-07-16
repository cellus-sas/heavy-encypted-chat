#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import SocketServer,sys,os
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
		else:
			path_trans_node=os.getcwd()+os.sep+"telecom_operator/trans.node"
	
		#print "trans node from l2r"+path_trans_node

		#print "data treatment local 2 remote"
		#need revers encoding url treatement 
		in_str= urllib.unquote(clear_text)
		
		#open key object #get ck
		#arg encrypted_content="",ck="",iv=0,difference="",h=""

		enc_obj=runkey.get_encrypted(unicode(in_str.decode('utf-8')))
		#print "enc obj from data treatment from l2r "+str(enc_obj)
		#answer > enctext,iv,d,h,ts
		#print enc_obj[0]
		try:
			pkl_file = open(path_trans_node, 'rb')
			trans_node_obj = pickle.load(pkl_file)
		except:
			#print "problem with opening receiv node"
			trans_node_obj=[]
		if enc_obj not in trans_node_obj:
			trans_node_obj.append(enc_obj)
		try:
			output = open(path_trans_node, 'wb')
			pickle.dump(trans_node_obj, output, -1)
			output.close()	
		except:
			#print "problem with saving receiv node"
			pass

		#ecnryption
		#ecriture dans le fichier telecom/trans.node
		#run.nowaitopenurlforging
		
		#print in_str

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
			required_field= self.data.split('GET /?&clear_text=')[1].split(' ')[0]
			# just send back the same data, but upper-cased
		except:
			#print "required_field error self.data='"+ self.data+"'"
			pass
		#try:
		self.data_treatment(clear_text=required_field)
		#except:
		#	#print "data is incorrect"
		#	pass
		#self.request.sendall(self.data.upper())
	
def do_job_loc_2_rem(HOST="localhost",PORT=9999):
	global random_port
	##print host
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
	do_job_loc_2_rem()
