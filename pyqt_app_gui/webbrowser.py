#!/usr/bin/env python
#before
import sys,time,os,subprocess,shlex
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
from multiprocessing import Process

local=True

class qtwebpage(object):

	def onDone(self,val):
		content= self.web.page().currentFrame().toHtml()
		print dir(content.fromLatin1)
		print "Done ...",val
		if self.autoClosedOnDone==True:
			self.web.close()
			#self.app.quit()
			#QTimer.singleShot(self.autoclosedDelay*1000, self.app.quit)
	    
	def onStart(self):
	    print "Started..."
	
	def onRefresh(self):
		print "Refreshing"
		self.web.setUrl(QUrl(self.url))
		QTimer.singleShot(5000, self.onRefresh)
		
	
	def open_webpage(self,url="http://www.whatsmyip.us/"):
		print "Load open webpage"
		self.app = QApplication(sys.argv)		
		print "Qapp init"
		self.url=url
		try:
			self.web = QWebView()
			self.web.loadStarted.connect(self.onStart)
			self.web.loadFinished.connect(self.onDone)
			self.settings = self.web.settings() # self.webView is the QWebView
			self.settings.setAttribute(QWebSettings.PluginsEnabled,True) 
			self.web.load(QUrl(self.url))
			self.web.resize(1024, 860)
			self.web.move(0, 0)
			self.web.setWindowTitle('Encrypted Chat with rotating timestamped keypass')
			self.web.show()
			print "Ok for init ... waiting Ondone event"
			
		except:
			pass
		QTimer.singleShot(5000, self.onRefresh)
		
		#QTimer.singleShot(15000, web.load)
		#QTimer.singleShot(15000, web.load)
		#QTimer.singleShot(60000, self.exit)
		#QTimer.singleShot(20000, self.login)
		self.app.exec_()
		print "Close ok"
		self.exit()
		return 0


	def dojob(self):
		return self.open_webpage(self.url)

	def __init__(self,url,autoClosedOnDone=False):
		self.autoClosedOnDone=autoClosedOnDone
		self.autoclosedDelay=1
		self.url=url
		print "Init > Start web page"
	
	def login(self):
		print "try login"


		time.sleep(0.5)
	
	def exit(self):
		self.app.quit()


import webbrowser

def do_ui(url):
	print dir(webbrowser)
	#webbrowser.open_new(url)

def start_ui():	
	global local
	if local==True:
	#filename="file://"+os.getcwd()+"/pyqt_app_gui/"+"localfile.html" #local call
		filename="ressource/localfile.html" #call from ../
	else:
		filename="ressource/localfile.html" #call from ../
#filename="file://"+os.getcwd()+"/ressource/localfile.html"
#	print "file:///home/noname/Bureau/Integrate_chat/pyqt-app-ui/localfile.html"
	print "run from "+os.getcwd()
	qtwebpage(url=filename,autoClosedOnDone=False).dojob()	
	#do_ui(filename)
if __name__ == "__main__":
	print "need be run "
	start_ui()
