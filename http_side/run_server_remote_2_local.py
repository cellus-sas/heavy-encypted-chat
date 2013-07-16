#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import SocketServer,sys,os
#import runkey
import random
import pickle
import base64
import runkey


local=False
random_port=False #debug
#print ('#handle request from remote client in order to decrypt the data then update json obj on local host')


#http://host:port/?&enc_text=&h=&t=
#10000
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def data_treatment(self,ed,h,d,distant_ip):
		global local

		#print "data treatment remote 2 local"
		#print ed,h,d
		if local==True:
			path_trans_node=os.getcwd()+os.sep+".."+os.sep+"telecom_operator/receiv.node"
		else:
			path_trans_node=os.getcwd()+os.sep+"telecom_operator/receiv.node"
		#print "data treatment"
		#print "trans node from r2l"+path_trans_node
		do_decod=False
		decoded_param=False
		try:
			ed=base64.b64decode(ed)
			ck=""
			iv=base64.b64decode(h)
			dtemp=d.split('-')
			d=dtemp[0]
			h=dtemp[1]
			ts=dtemp[2]
			decoded_param=True
			#print "good parameter decoded"
		except:
			decoded_param=False
			#print "no good data parameter"

		if decoded_param==True:
			#print "get runkey"
			rts=runkey.get_ck_from_obj()
			#print "run key ok!"
			if int(rts[1])==int(ts):
				#print "do decod True"
				do_decod=True
				ck=""
			else:
				#print "Difference between current key and timestamp in received data"
				##print " trying get key from timestamp"
				day=rts[0]
				#day="130708"
				tempk=runkey.get_ck_from_timestamp(ts=ts,day=day) #rts[0] mean day from current key problem si changement de jour
				ck=tempk[-1]
				if ck!="":
					do_decod=True
		else:
			do_decod=False
		if do_decod==True:
			##print "runkey"
			#print "decoding"
			
			#print "ed >"+ed+"cool"
			#print ck
			#print iv
			#print d
			#print h
			#print ts
			##print "ed,ck ... >"+str(ed,ck,iv,d,h,ts)
			#print "enter decodin in runkey get decrypted"
			decoding= runkey.get_decrypted(encrypted_content=ed,ck=ck,iv=iv,difference=d,h=h)
			#print "decoding content next line"
			#print decoding
			#print "decoded > "+str(decoding.encode('utf-8'))###maybay dont need unicode
			##print "end runkey"
		else:
			#print "no decoding <<<<<<<<<<<<<<<<<<<<<<<"
			decoding=""
		#print "do dec_obj"
		try:
			dec_obj=[decoding.decode('latin-1').encode('utf-8'),ts,distant_ip] #work with conventional 
		except:
			dec_obj=[decoding.encode('utf-8'),ts,distant_ip] #work with conventional 
		#print "do dec obj ok!"
		#print "dec_obj "+str(dec_obj)
		receiv_node_obj=[]
		try:
			pkl_file = open(path_trans_node, 'rb')
			trans_node_obj = pickle.load(pkl_file)
		except:
			#print "problem with opening trans node"
			pass
			
		if dec_obj not in trans_node_obj:
		#ajoute la ligne dans receiveobj
			trans_node_obj.append(dec_obj)
		try:
			output = open(path_trans_node, 'wb')
			pickle.dump(trans_node_obj, output, -1)
			output.close()	
		except:
			#print "problem with saving trans node"
			pass

		#ecnryption
		#ecriture dans le fichier telecom/trans.node
		#run.nowaitopenurlforging
		
		#print clear_text

		
    def handle(self):
        #print os.getcwd()
        try:
			with open(os.getcwd()+os.sep+'http_side'+os.sep+'exit_remote_2_local','r') as f:
				f.read()
			sys.exit()
        except:
			pass
			
        #print "handel"
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        distant_ip = format(self.client_address[0])
        #print distant_ip
        try:
	        required_field= self.data.split('GET /?&enc_text=')[1].split(' ')[0]
	        ##print "required_field "+required_field
	        encrypted_data= required_field.split('&h=')[0]
        except:
	        ##print self.data
	        pass
        try:
	        h= required_field.split('&h=')[1]
	        d= h.split('&d=')[1]
	        h=h.split('&d=')[0]
	        self.data_treatment( encrypted_data,h,d,distant_ip )
	        #print encrypted_data,h,d,required_field
        except:
			pass
		#push data to treatement

        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


def do_job_rem_2_loc(HOST="localhost",PORT=10000):
	global random_port
	#print host
	if random_port==True:
		PORT=random.randint(8000,12000)
		print "random port is "+str(PORT)
	# Create the server, binding to localhost on port 10000
	SocketServer.TCPServer.allow_reuse_address = True
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
	
	
if __name__ == "__main__":
	global local,random_port
	random_port=True
	local=True
	print "need be run "
	do_job_rem_2_loc()
