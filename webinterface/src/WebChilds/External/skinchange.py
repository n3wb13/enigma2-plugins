from Components.config import config, ConfigSubsection, configfile, ConfigPassword, ConfigText, getConfigListEntry, ConfigSelection
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Sources.List import List
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.Sources.Source import Source
import Components.Harddisk
from Tools.Directories import fileExists
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_ACTIVE_SKIN
from Tools.LoadPixmap import LoadPixmap
from Screens.Standby import *
from enigma import eTimer, eEnv
from os import path, mkdir
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
from Components.Sources.StaticText import StaticText


header_string = ''
header_string += '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"'
header_string += '"http://www.w3.org/TR/html4/loose.dtd">'
header_string += '<head>'
header_string += '<meta content="text/html; charset=UTF-8" http-equiv="content-type"><META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">'
header_string += '</head><body><font color="#485052" >'
tself = 'target="_self"'

global infoList	

def checkSkin(objelt):
	SKINXML = "skin.xml"
	DEFAULTSKIN = "< Default >"
	PICONSKINXML = None
	PICONDEFAULTSKIN = None
	NFRSKINXML = None
	NFRDEFAULTSKIN = None	
	skinlist = []
	root = os.path.join(eEnv.resolve("${datadir}"),"enigma2")
	#config = config.skin.primary_skin
        infoList = []
        zeilen = list()
        if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data/skin"):
                os.system("rm /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data/skin/*.*")
        else:
                mkdir("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data/skin")
        try:
                for root, dirs, files in os.walk(root, followlinks=True):
			for subdir in dirs:
				dir = os.path.join(root,subdir)
				if os.path.exists(os.path.join(dir,SKINXML)):
				        pngpath = os.path.join(os.path.join(root, subdir), "prev.png")
					webpngpath = "/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data/skin/" + subdir + ".png" 
                                        shutil.copyfile(pngpath, webpngpath)
                                        skinlist.append(subdir)
			dirs = []
         
	finally:
	        skinlist.append("Default")
		infoList = skinlist 
        return infoList

class SkinChange(resource.Resource):
    
	def render_GET(self, req):
		global infoList
		root = os.path.join(eEnv.resolve("${datadir}"),"enigma2")
        	change = '<input style="color&#58;#00b000;" type="submit" value="Change Skin">'
        	req.setResponseCode(http.OK)
        	req.setHeader('Content-type', 'text/html')
        	req.setHeader('charset', 'UTF-8')
        	infoList = checkSkin(None)
        	html = header_string        	
        	#if  "no Backgroundimage found!" in infoList:
                #        html += '<center><table style="width: 100%%;table-layout: fixed;" border="0" cellspacing="0"><tr><td align="left">NO Backgroundimage found</td></tr></center>'
                #        self.finished()
                #else: 
        	for info in infoList:
       			addExternalChild(('%sstart' % info, SkinSel(info)))
       			pngpath = "/web-data/skin/" + info + ".png"
      			Images = '<a href="%sstart" target="_self">%s</a></form>' % (info, change)
         		html += '<center><table style="width: 80%%;table-layout: fixed;" border="0" cellspacing="0"><tr><td align="left">%s:</td><td><img src="%s" width="100%%" height="100%%" align="left"></td><td align="right">%s</td></tr></center>' % (info, pngpath, Images) 
        
                return html
        	
 	def finished(self):
        	print 'finished'

class SkinSel(resource.Resource):
    
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
                info = self.input
        	addExternalChild(('%sstart' % info, SkinGui(info)))
        	html += '<center>Change Skin and Restart Gui!<a href="%skill" target="_self"><input type="submit" value="Change"></a><p></p><p></p></center>' % (info)
        	html += '<center>Nothing Change and back!<a href="javascript:location.reload()" target="_top"><input type="submit" value="back"></a></center>'
        	return html
    
	def finished(self, retval):
        	print 'finished', retval

class SkinGui(resource.Resource):
    
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
        		        config.skin.primary_skin.setValue(eEnv.resolve("${datadir}/enigma2/" + self.input + "/skin.xml"))
        		        config.skin.primary_skin.save()
        		        configfile.save()
        		        from Screens.Standby import TryQuitMainloop
				quitMainloop(3)
				return "true"
                		continue
        		html += '<p></p>'
        	return html

	def finished(self, retval):
        	print 'finished', retval


addExternalChild(('SkinChange', SkinChange()))
infoList = checkSkin(None)
for info in infoList:
	addExternalChild(('%sstart' % info, SkinSel(info)))
	addExternalChild(('%skill' % info, SkinGui(info)))
