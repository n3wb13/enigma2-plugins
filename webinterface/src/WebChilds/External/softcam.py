from Components.ActionMap import ActionMap
from Components.config import config, ConfigSubsection, configfile, ConfigPassword, ConfigText, getConfigListEntry, ConfigSelection
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from Components.ScrollLabel import ScrollLabel
from Components.About import about
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer
from os import path
import os
from Plugins.Extensions.Infopanel import Softcam
import sys
import struct
import stat
from twisted.web import resource, http
from Plugins.Extensions.WebInterface.WebChilds.Toplevel import addExternalChild
import commands
from os import path as os_path, symlink, listdir, unlink, readlink, remove, system
from commands import getoutput
from enigma import eConsoleAppContainer, gMainDC
from Screens.Standby import TryQuitMainloop
import socket
import subprocess

header_string = ''
header_string += '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'
header_string += '"http://www.w3.org/TR/html4/loose.dtd">'
header_string += '<head>'
header_string += '<meta content="text/html; charset=UTF-8" http-equiv="content-type"><META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">'
header_string += '</head><body><font color="#485052" >'
tself = 'target="_self"'
cammessage = '<center>Bitte erst die Aktive SoftCam beenden! <a href="SoftcamControl" target="_self"><input type="submit" value="Zur&uuml;ck"></a></center>'
camdkil = '<a href="camdkill"'
config.NFRSoftcam = ConfigSubsection()
config.NFRSoftcam.actcam = ConfigText(visible_width = 200)
config.NFRSoftcam.actCam2 = ConfigText(visible_width = 200)
config.NFRSoftcam.waittime = ConfigSelection([('0',_("dont wait")),('1',_("1 second")), ('5',_("5 seconds")),('10',_("10 seconds")),('15',_("15 seconds")),('20',_("20 seconds")),('30',_("30 seconds"))], default='15')
config.NFRSoftcam.camdir = ConfigText(default = "/usr/emu", fixed_size=False)
config.NFRSoftcam.camconfig = ConfigText(default = "/usr/keys", fixed_size=False)
global infoList	
global ownip
def checkCams(objelt):
        infoList = []
        if os.path.isfile('/etc/emulist'):
                print "emulist found"
        else:
                os.system('echo "no Softcam installed" >/etc/emulist')        
        f = open("/etc/emulist", 'r')
        zeilen = list()
        try:
		for line in f:
			zeilen.append(line.strip())
	finally:
		f.close()
       	infoList = zeilen	
        return infoList
        

def createip(objelt):
	#self.iface = "eth0"
	eth0 = about.getIfConfig('eth0')
	if eth0.has_key('addr'):
		ownip = eth0['addr']
		#self.iface = 'eth0'

	eth1 = about.getIfConfig('eth1')
	if eth1.has_key('addr'):
		ownip = eth1['addr']
		#self.iface = 'eth1'

	ra0 = about.getIfConfig('ra0')
	if ra0.has_key('addr'):
		ownip = ra0['addr']
		#self.iface = 'ra0'

	wlan0 = about.getIfConfig('wlan0')
	if wlan0.has_key('addr'):
		ownip = wlan0['addr']
		#self.iface = 'wlan0'
        return ownip

class SoftcamControl(resource.Resource):
    
	def render_GET(self, req):
	        self.Console = Console()
		global infoList
		act_webif = False
        	infoList = checkCams(None)
        	aktiv = '<input style="background-color&#58;#00b000;" type="button" value="Aktiviert">'
        	webaktivieren = '<input style="color&#58;#00b000;" type="submit" value="Open Cam Webif">'
                aktivieren = '<input style="color&#58;#00b000;" type="submit" value="Aktivieren">'
        	deaktivieren = '<input style="color&#58;#FF0000;" type="submit" value="Deaktivieren">'
       		deaktiviert = '<input style="background-color&#58;#FF0000;" type="button" value="Deaktiviert">'
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	self.activecam = False
        	self.actcam = config.NFRSoftcam.actcam.value
        	camconfigs = []
        	ps = subprocess.Popen(('ps', 'ax'), stdout=subprocess.PIPE)
        	output = ps.communicate()[0]
        	for line in output.split('\n'):
            	    if self.actcam in line:
                        t = line.find("keys")
                        t1 = len(line)
                        camconfigs.append(line[t:t1])
                        self.activecam = True
        	
                if self.activecam == False:
                    print "no Softcam Activ!"
                    #self.actcam = "None"
                else:
                    if 'doscam' in self.actcam:
                        searchfile = camconfigs[0] + '/doscam.cfg'
                    elif 'oscam' in self.actcam: 
                        searchfile = camconfigs[0] + '/oscam.conf' 
                    elif 'cccam' in self.actcam or 'CCcam' in self.actcam: 
                        searchfile = camconfigs[0]
                    if 'oscam' in self.actcam or 'doscam' in self.actcam or 'cccam' in self.actcam or 'CCcam' in self.actcam:
                        fdc = open('/usr/' + searchfile) 
                        zeilencfg = fdc.read().split('\n')
                        fdc.close()
                        for line in zeilencfg:
                            if line.startswith("WEBINFO") or line.startswith("httpport"):
                                newline = line.rsplit(" ", 1)
                                act_webif = True
        	camdinfo = ''
        	html = header_string
        	for info in infoList:
       		    addExternalChild(('%sstart' % info, CamdStart(info)))
        	    addExternalChild(('%skill' % info, CamdKill(info)))
        	    if info == self.actcam:
        	        if 'oscam' in self.actcam or 'doscam' in self.actcam or 'cccam' in self.actcam or 'CCcam' in self.actcam:
                            if act_webif == True:
                                camd = '%s<a href="%skill" target="_self">%s</a>' % (aktiv, info, deaktivieren)
                                #camd = '%s<a href="%skill" target="_self">%s</a></td><td align="right">%s_Webif<a href="http://%s:%s" target="_blank">%s</a>' % (aktiv, info, deaktivieren, self.actcam, ownip, newline[1], webaktivieren)
                                html += '<center><table style="width: 80%%;table-layout: fixed;" border="1" cellspacing="0"><tr><td align="center">%s_Webif<a href="http://%s:%s" target="_blank">%s</a></td></tr></center>' % (self.actcam, ownip, newline[1], webaktivieren)
                            else:
                                camd = '%s<a href="%skill" target="_self">%s</a>' % (aktiv, info, deaktivieren)
                        else:
                            camd = '%s<a href="%skill" target="_self">%s</a>' % (aktiv, info, deaktivieren)
        	    else:   
                	camd = '<a href="%sstart" target="_self">%s</a>%s</form>' % (info, aktivieren, deaktiviert)
        	    html += '<center><table style="width: 80%%;table-layout: fixed;" border="1" cellspacing="0"><tr><td align="left">%s:</td><td align="right">%s</td></tr></center>' % (info, camd)
        	    
                if os.path.isfile('/tmp/ecm.info'):
        	    fd = open('/tmp/ecm.info')
       		    for line in fd:
                	print line
                	html += '<center><table align="center" style="width: 50%%;" border="1" cellspacing="0"><tr><td>%s</font></td></tr></table></center>' % line
            
        	else:
        	    html += '<center><table style="width: 50%%;" border="1" cellspacing="0"><tr><td><font color="#a1a1a1">ECM Info N/A</font></td></tr></table></center>'
        	return html



class CamdStart(resource.Resource):
    
	def __init__(self, input):
	        self.Console = Console()
	        self.camstartcmd = ""
        	self.container = eConsoleAppContainer()
        	self.container.appClosed.append(self.finished)
        	self.actcam = config.NFRSoftcam.actcam.value
        	self.input = input

    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	for info in infoList:
        	    if info == self.input:
        	        self.camstartcmd = Softcam.getcamcmd(self.input)
 			self.activityTimer = eTimer()
			self.activityTimer.timeout.get().append(self.stopping)
			self.activityTimer.start(1000, False) 
                	#self.container.execute(info)
                	html += '<center>%s erfolgreich Gestartet!  <a href="SoftcamControl" target="_self"><input type="submit" value="Zur&uuml;ck"></a></center>' % self.input
                	continue
        	    html += '<p></p>'
        	return html

    
	def finished(self, retval):
        	print 'finished', retval
        	
        	
	def stopping(self):
		self.activityTimer.stop()
		self.actcam = config.NFRSoftcam.actcam.value
		Softcam.stopcam(self.actcam)
		print "[NFR-SoftCam Manager stop] ", self.actcam
		cmd = "killall -15 " + self.actcam
                self.Console.ePopen(cmd)
		self.actcam = self.input
		if config.NFRSoftcam.actcam.value != self.actcam: 
			config.NFRSoftcam.actcam.value = self.actcam
			print "[save actcam] ", self.actcam
			config.NFRSoftcam.actcam.save()
			configfile.save()
		#config.NFRSoftcam.actcam.save()	
                #configfile.save()	
		self.Console.ePopen(self.camstartcmd)
		print "[NFR-SoftCam Manager] ", self.camstartcmd


class CamdKill(resource.Resource):
    
	def __init__(self, input):
	        self.Console = Console()
        	self.container = eConsoleAppContainer()
        	self.container.appClosed.append(self.finished)
        	self.actcam = config.NFRSoftcam.actcam.value
        	self.input = input  

    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	for info in infoList:
        	    if info == self.input:
                	cmd = "killall -15 " + self.input
                	self.Console.ePopen(cmd)
                	config.NFRSoftcam.actcam.value = ""
			config.NFRSoftcam.actcam.save()
			configfile.save()
                	html += '<center>%s erfolgreich beendet!  <a href="SoftcamControl" target="_self"><input type="submit" value="Zur&uuml;ck"></a></center>' % self.input
                	continue
        	    html += '<p></p>'
        	return html

    
	def finished(self, retval):
        	print 'finished', retval


addExternalChild(('SoftcamControl', SoftcamControl()))
infoList = checkCams(None)
ownip = createip(None) 
for info in infoList:
	addExternalChild(('%sstart' % info, CamdStart(info)))
	addExternalChild(('%skill' % info, CamdKill(info)))
