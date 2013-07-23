import os,sys,subprocess
local=False

def do_job_rungui():
	global local

	if local==True:
		path_ressource=os.getcwd()+os.sep+".."+os.sep+"gui"+os.sep
	else:
		path_ressource=os.getcwd()+os.sep+"gui"+os.sep
	

	d=path_ressource+"ressource/localfile.html"
	if sys.platform=='win32':
	    subprocess.Popen(['start', d], shell= True)
	
	elif sys.platform=='darwin':
	    subprocess.Popen(['open', d])
	
	else:
	    try:
	        subprocess.Popen(['xdg-open', d])
	    except OSError:
			pass
	        # er, think of something else to try
	        # xdg-open *should* be supported by recent Gnome, KDE, Xfce
	
if __name__ == "__main__":
	global local
	local=True
	#print "need be run "
	do_job_rungui()
