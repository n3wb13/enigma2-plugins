from Components.ActionMap import ActionMap, NumberActionMap
from Components.config import config, ConfigSubsection, configfile, ConfigPassword, ConfigText, getConfigListEntry, ConfigSelection
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button
from Components.MenuList import MenuList
from Components.Input import Input
from Components.ProgressBar import ProgressBar
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
import Components.Harddisk
from Tools.Directories import fileExists
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap

from enigma import eTimer
from os import path
import os
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

global infoList	

def checkImages(objelt):
        infoList = []
        zeilen = list()
        try:
                pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/NFR4XBoot'
                f = open(pluginpath + '/.nfr4xboot_location', 'r')
                mypath = f.readline().strip()
                f.close()
        except:
                mypath = '/media/hdd'
                
        try:
                mypath2 = mypath + 'NFR4XBootI/'
                myimages = os.listdir(mypath2)
                for fil in myimages:
                        if os.path.isdir(os.path.join(mypath2, fil)):
                                zeilen.append(fil)
	finally:
		infoList = zeilen                                
        return infoList

class MultibootControl(resource.Resource):
    
	def render_GET(self, req):
		global infoList
        	booten = '<input style="color&#58;#00b000;" type="submit" value="Booten">'
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	infoList = checkImages(None)
        	html = header_string
        	for info in infoList:
       		    addExternalChild(('%sstart' % info, ImageStart(info)))
        	    Images = '<a href="%sstart" target="_self">%s</a></form>' % (info, booten)
         	    html += '<center><table style="width: 80%%;table-layout: fixed;" border="1" cellspacing="0"><tr><td align="left">%s:</td><td align="right">%s</td></tr></center>' % (info, Images)
        	return html


class ImageStart(resource.Resource):
    
	def __init__(self, input):
	        self.Console = Console()
	        self.imagestartcmd = ""
        	self.container = eConsoleAppContainer()
        	self.container.appClosed.append(self.finished)
        	self.input = input
        	print 'self.input', self.input

    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	for info in infoList:
        		if info == self.input:
        			out = open('/media/nfr4xboot/NFR4XBootI/.nfr4xboot', 'w')
        			out.write(self.input)
        			out.close()
        			os.system('rm /tmp/.nfr4xreboot')
                                os.system('touch /tmp/.nfr4xreboot')
                                os.system('reboot -p')        	    
                		html += '<center>%s erfolgreich Gestartet!  <a href="MultibootControl" target="_self"><input type="submit" value="Zur&uuml;ck"></a></center>' % self.input
                		continue
        		html += '<p></p>'
        	return html

    
	def finished(self, retval):
        	print 'finished', retval




addExternalChild(('MultibootControl', MultibootControl()))
infoList = checkImages(None)
for info in infoList:
	addExternalChild(('%sstart' % info, ImageStart(info)))
