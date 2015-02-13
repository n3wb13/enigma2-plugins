from Components.ActionMap import ActionMap
from Components.config import config, ConfigSubsection, configfile, ConfigPassword, ConfigText, getConfigListEntry, ConfigSelection
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from Components.ScrollLabel import ScrollLabel
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
def checkCams(objelt):
        infoList = []
        if os.path.isfile('/etc/emulist'):
                print "emilist found"
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

class SoftcamControl(resource.Resource):
    
	def render_GET(self, req):
		global infoList
        	aktiv = '<input style="background-color&#58;#00b000;" type="button" value="Aktiviert">'
        	aktivieren = '<input style="color&#58;#00b000;" type="submit" value="Aktivieren">'
        	deaktivieren = '<input style="color&#58;#FF0000;" type="submit" value="Deaktivieren">'
       		deaktiviert = '<input style="background-color&#58;#FF0000;" type="button" value="Deaktiviert">'
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	self.actcam = config.NFRSoftcam.actcam.value
        	infoList = checkCams(None)
        	camdinfo = ''
        	html = header_string
        	for info in infoList:
       		    addExternalChild(('%sstart' % info, CamdStart(info)))
        	    addExternalChild(('%skill' % info, CamdKill(info)))
        	    if info == self.actcam:
        	    #if info[2] == 'yes':
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
        	print 'self.input', self.input

    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	print "Infolist:", infoList
        	for info in infoList:
        	    if info == self.input:
        	        self.camstartcmd = Softcam.getcamcmd(self.input)
 			self.activityTimer = eTimer()
			self.activityTimer.timeout.get().append(self.stopping)
			self.activityTimer.start(100, False)       	        
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
for info in infoList:
	addExternalChild(('%sstart' % info, CamdStart(info)))
	addExternalChild(('%skill' % info, CamdKill(info)))

