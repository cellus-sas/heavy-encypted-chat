#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#need easy_install ntplib
#sudo apt-get install python-crypto
import datetime,time,sys,os

import pprint, pickle
import ntplib

import thread
import threading



useNTPserversync=True
update_time_NTPserversync_delay=400 #second between time correction algo
deported_time=False
deport_time_day=0 #0-x
deport_time_hour=9 #0-24
deport_time_minute=30 #0-59
deport_time_second=0 #0-59
deport_time_microsecond=0 #0-999999

next_key_approching_dt=3 # 5 for 
default_apprach_dt=0.001 #between 0.2 to 0.001> 0.1 is ok
default_dt=0.5 #0.5 for seconds changing / #

loop_dt=''
key_dir_path=''

exiting_there=False
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)


#get real time from ntp server on line
def get_real_timedate():
	table_ntp_server=['fr.pool.ntp.org']
	x = ntplib.NTPClient()
	try:
		answer=datetime.datetime.utcfromtimestamp(x.request(str(table_ntp_server[0])).tx_time)
	except:
		print "ERROR:> no connectivity to "+str(table_ntp_server)
		sys.exit()
		answer=""
	return answer

#set real timedate with timedelta(from get real timedate) apply
def set_real_timedate():
	global deport_time_day,deport_time_hour,deport_time_minute,deport_time_second,deport_time_microsecond,deported_time
	rt=get_real_timedate()
	ost=datetime.datetime.now()
	real_delay=ost-rt
	#print "dt between legal time " + str(real_delay.total_seconds())
	deport_time_day=0 #0-x
	deport_time_hour=0 #0-24
	deport_time_minute=0 #0-59
	deport_time_second=-real_delay.total_seconds() #0-59
	deport_time_microsecond=real_delay.microseconds #0-999999
	deported_time=True

def update_time_delay(arg1='',arg2=''):
	global update_time_NTPserversync_delay
	global exiting_there
	print "************************* SET TIME DELAY according to real time getin wiht ntp \n"
	set_real_timedate()
	#print "*************************updating via ntp is ok<"
	time.sleep(update_time_NTPserversync_delay)
	if exiting_there==False:
		update_time_delay()

def millis():
    return int(str(int(round(time.time() * 1000)))[-3:])


def convert_datetime_2_timestamp(date):
	part_a=str(date).split(' ')[0].replace('-','')
	part_b=date.hour*3600+date.minute *60+date.second
	return part_a,part_b

def getdatetime():
	global deported_time,deport_time_day,deport_time_hour,deport_time_minute,deport_time_second,deport_time_microsecond
	if deported_time==True:
		rt=datetime.datetime.now()
		td=datetime.timedelta(days=deport_time_day, seconds=deport_time_second, microseconds=deport_time_microsecond, milliseconds=0, minutes=deport_time_minute, hours=deport_time_hour, weeks=0)
		d=rt+td
	else:
		d=datetime.datetime.now()
	return d

def loadtable(file_table):
	pkl_file = open(file_table, 'rb')
	table = pickle.load(pkl_file)
	return table

def loadcurrentday_table(delta_day=0):		
	global local,key_dir_path
	d=getdatetime()+datetime.timedelta(days=delta_day)
	obj_t= convert_datetime_2_timestamp(d)
	pkl_filename=obj_t[0]
	if len(pkl_filename)==8:
		pkl_filename=pkl_filename[2:]
	
	if local==True:
		table=loadtable('key/'+pkl_filename+'.pkl') #local
	else:
		if key_dir_path!='':
			table=loadtable(key_dir_path+os.sep+pkl_filename+'.pkl')
		else:
			table=loadtable('crypto_client/key/'+pkl_filename+'.pkl') #from ../	
	return table



def write_current_key(key_obj):
	output = open('current_key.pkl', 'wb')
	pickle.dump(key_obj, output, -1)
	output.close()	

def do_key_regeneration_job(key_dir_path_arg=""):
	global key_dir_path
	key_dir_path=key_dir_path_arg
	
	global exiting_there
	global useNTPserversync
	global update_time_NTPserversync_delay
	global deported_time
	global deport_time_day
	global deport_time_hour
	global deport_time_minute
	global deport_time_second
	global deport_time_microsecond
	
	global next_key_approching_dt
	global default_apprach_dt
	global default_dt
	
	global loop_dt
	
	current_key_value=''
	
	next_key_is_focused=False
	next_key_approching=False
	next_key_is_reach=False
	next_timestamp=0
	next_i=0
	
	next_day_approching=False
	pre_next_day_is_reach=False
	next_day_is_reach=False
	next_day_now=False
	table_yesterday=[]
	table_today=[]
	
	table=loadcurrentday_table()  
	table_today=table
	next_day_cp=0
	
	correction=0
	
	draw_l=""
	
	if useNTPserversync==True:
		print "starting refresh with ntp thread"
		thread_refresh_with_ntp=FuncThread(update_time_delay)
		thread_refresh_with_ntp.start()
		set_real_timedate()
		
	if deported_time==True:
		print "deported time"
	print "Starting"
	exiting=False
	firstrun=True
	while exiting==False:
		#loop_start_dt=datetime.datetime.now()
		if next_day_approching==False:
			table=table_today
			pass
		else:
			table=table_yesterday
			
	
		t_info= convert_datetime_2_timestamp(getdatetime())

		cu_dt=default_dt
		
		if next_key_is_focused==False or next_key_is_reach==True or next_day_is_reach==True:
			if next_day_approching==True:
				if pre_next_day_is_reach==True:
					next_day_cp=next_day_cp+1
					if next_day_cp==2:
						#print "focused new key with next_day_approching=True"
						next_day_now=True
						next_day_approching=False
						next_day_is_reach=False
						pre_next_day_is_reach=False
						table=table_today
						cu_dt=default_apprach_dt
						next_i=0
						dt_changing_key=0
	
			for i in range(next_i,len(table)):
				if int(table[i][1])>int(t_info[1]):
					next_timestamp=int(table[i][1])
					next_i=i
					dt_changing_key=int(table[i][1])-int(t_info[1])
					current_key=table[i-1]
					current_key_value = current_key[2]
					#print "key found" #+ str(table[i-1])
					#print "next key is "+str(table[i])
					#print "change key in " + str(dt_changing_key) +"s" 
					next_key_is_focused=True
					next_key_approching=False
					next_key_is_reach=False
					#print "current key ID:" + str(current_key[1]) +" VALUE:'"+ current_key_value +"'"
					write_current_key(current_key)
					d=str(datetime.datetime.now())


					print "> encrypted key changed at \n  [ostime:"+d+"\n  [softwaretime:"+str(getdatetime())+"]"
					break
				
		else:

			dt_changing_key=next_timestamp-int(t_info[1])
			#dt_changing_key=[dt_changing_key_fullobj[0],dt_changing_key_fullobj[1]]
				
			if dt_changing_key<=next_key_approching_dt:
				#print "approching changing"
				#print "change key to "+ str(table[i][1]) +" in " + str(dt_changing_key) +"s" 	
				#if dt_changing_key!=0:
					#draw="change key to "+ str(table[i][1]) +" in " + str(dt_changing_key) +"s" 	
				#	if draw!=draw_l:
				#		draw_l=draw
				#		print draw	
				#print dt_changing_key_fullobj[3]
				next_key_approching=True
				cu_dt=default_apprach_dt
				#modify time_sleep
				if dt_changing_key<=1:
					#print milli
					#print "high precision runnuer \n [ostime:"+str(datetime.datetime.now())+"\n [softwaretime:"+str(getdatetime())+"]"
					cu_dt=float(default_apprach_dt)/10.0
					#print cu_dt
						
					if dt_changing_key<=0:
						#print "changing key now! [real:"+str(getdatetime())+" / local:"+str(datetime.datetime.now())+"]"
						#print "change key to "+ str(table[i][1]) 
						next_key_is_reach=True
						cu_dt=0

				
			pass
			
		if cu_dt==default_dt:
			try:
				#draw="change key to "+ str(table[i][1]) +" in " + str(dt_changing_key) +"s"
				if draw!=draw_l:
					draw_l=draw
					print draw
				pass
			except:
				pass
		else:
			pass
			
		if next_i>len(table)-3:
			print "> changing day db prepare"
			if next_day_approching==False:
				table_yesterday=table
				try:
					print "loading next day"
					table_today=loadcurrentday_table(1)
				except:
					pass
				next_day_approching=True
	
			if next_i==len(table)-1:
				print " > critical before changing day"
				pre_next_day_is_reach=True
		
		#let possibility to be exiting by outside
		#try:
		#	with open(os.getcwd()+os.sep+'crypto_client'+os.sep+'exit_run','r') as f:
		#		f.read()
		#	break
		#	exiting=True
		#	exiting_there=True
		#	sys.exit()
		#except:
		#	pass		
		#print cu_dt
		#print loop_dt
		#loop_end_dt=datetime.datetime.now()
		#loop_dt= loop_end_dt- loop_start_dt
		#print loop_dt.microseconds/1000
		time.sleep(cu_dt)
	
	
	if useNTPserversync==True:
		print "exiting refresh with ntp thread"
		thread_refresh_with_ntp.exit()
local=False
if __name__ == "__main__":
	global local
	print "need be run "
	local=True
	do_key_regeneration_job()
	
