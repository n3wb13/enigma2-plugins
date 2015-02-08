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
from Screens.Standby import *

from enigma import *
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
import shutil

header_string = ''
header_string += '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'
header_string += '"http://www.w3.org/TR/html4/loose.dtd">'
header_string += '<head>'
header_string += '<meta content="text/html; charset=UTF-8" http-equiv="content-type"><META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">'
header_string += '</head><body><font color="#485052" >'
tself = 'target="_self"'

global infoList	

def checkKeymap(objelt):
        infoList = []
        zeilen = list()
        try:
                backpath = '/usr/share/enigma2/'
                if os.path.exists(backpath):
                        mykeymaps = os.listdir(backpath)
                        for fil in mykeymaps:
                                if "keymap" in fil:
                                        zeilen.append(fil)
                                else:                                        
                                        pass                
                else:
                        zeilen.append("no Keymap found!")                                        
	finally:
		infoList = zeilen                                
        return infoList

class KeymapChange(resource.Resource):
    
	def render_GET(self, req):
		global infoList
        	change = '<input style="color&#58;#00b000;" type="submit" value="Change Keymap">'
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	infoList = checkKeymap(None)
        	html = header_string        	
        	if  "no Keymap found!" in infoList:
                        html += '<center><table style="width: 100%%;table-layout: fixed;" border="0" cellspacing="0"><tr><td align="left">NO Keymap found</td></tr></center>'
                        self.finished()
                else: 
        		for info in infoList:
       		    		addExternalChild(('%sstart' % info, KeymapCP(info)))
        	    		Keymaps = '<a href="%sstart" target="_self">%s</a></form>' % (info, change)
         	    		html += '<center><table style="width: 80%%;table-layout: fixed;" border="1" cellspacing="0"><tr><td align="left">%s:</td><td align="right">%s</td></tr></center>' % (info, Keymaps)
                return html
        	
 	def finished(self):
        	print 'finished'

class KeymapCP(resource.Resource):
    
	def __init__(self, input):
	        self.Console = Console()
	        self.imagestartcmd = ""
        	self.container = eConsoleAppContainer()
        	self.container.appClosed.append(self.finished)
        	self.input = input

    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	addExternalChild(('%sstart' % info, KeymapGui(info)))
        	#Keymaps = '<a href="%skill" target="_self">Change and Guirestart</a></form>' % (info)
         	#html += '<center><table style="width: 80%%;table-layout: fixed;" border="1" cellspacing="0"><tr><td align="left">%s:</td><td align="right">%s</td></tr></center>' % (info, Keymaps)
                html += '<center>Change Keymap and Restart Gui!<a href="%skill" target="_self"><input type="submit" value="Change"></a><p></p><p></p></center>' % (info)
                html += '<center>Nothing Change and back!<a href="javascript:location.reload()" target="_top"><input type="submit" value="back"></a></center>'
        	return html

    
	def finished(self, retval):
        	print 'finished', retval

class KeymapGui(resource.Resource):
    
	def __init__(self, input):
	        self.Console = Console()
	        self.imagestartcmd = ""
        	self.container = eConsoleAppContainer()
        	self.container.appClosed.append(self.finished)
        	self.input = input
    
	def render_GET(self, req):
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	html = header_string
        	for info in infoList:
        		if info == self.input:
        		        config.usage.keymap.setValue(eEnv.resolve("${datadir}/enigma2/" + self.input))
        		        config.usage.keymap.save()
        		        configfile.save()
        		        quitMainloop(3)
                		continue
        		html += '<p></p>'
        	return html

	def finished(self, retval):
        	print 'finished', retval

addExternalChild(('KeymapChange', KeymapChange()))
infoList = checkKeymap(None)
for info in infoList:
	addExternalChild(('%sstart' % info, KeymapCP(info)))
	addExternalChild(('%skill' % info, KeymapGui(info)))
