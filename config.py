#!/usr/bin/python

import os
import threading
import xmpp
import sys

class socketMessage():
	def __init__(self,s,socket=None):
		self.message=s
		self.socket=socket
	
	def send(self):
		try:
			self.socket.send(self.message)
		except:
			pass
	
	def getBody(self):
		return self.message

class configurator():
	def __init__(self,daemon=None):
		self.d=daemon
		self.configfile='config.ini'
		if (len(sys.argv)>0):
			self.configfile=sys.argv[1]
		self.conf = self.loadConfig(self.configfile)

		self.plugins={}
		self.plugins['commands']=self.loadUnitsList('commands')
		self.plugins['socket']=self.loadUnitsList('socket')
	
	def getDynamicPlugin(self,ptype,pname):
		if (self.plugins[ptype][pname]==None):
			unit=__import__('plugins.'+ptype+'.'+pname)
			unit=getattr(unit,ptype)
			unit=getattr(unit,pname)
			try:
				unit.d=d
			except:
				pass
			cl=getattr(unit,pname+'_plugin')
			unit.p=cl(self,self.d)
			self.plugins[ptype][pname]=unit
		else:
			unit=self.plugins[ptype][pname]
		return unit
	
	def execPluginFunction(self,unit,fname,mess,query=None):
		if (unit.p.allowed.has_key(fname)):
			print "Executing `"+fname+"` function"
			command = getattr(unit.p,fname)
			res=None
			if (unit.p.allowed[fname].has_key('thread')and(unit.p.allowed[fname]['thread'])):
				t=threading.Thread(target=command,args=(mess,query))
				t.start()
			else:
				res=command(mess,query)
			return res
		else:
			print "Function `"+fname+"` is not allowed"


			


	def loadUnitsList(self,ptype):
		units={}
		for unit in os.listdir('plugins/'+ptype+'/'):
			if unit.endswith('.py'):
				unit_name = unit[:-3]
				if (unit_name != '__init__'):
					units[unit_name] = None
		return units


	def loadConfig(self,filename):
		import ConfigParser
		config = ConfigParser.ConfigParser()
		config.read(filename)
		jid = config.get('connection', 'jid')
		password = config.get('connection', 'password')
		c={'jid':jid,'password':password}
		c['socket']={}
		try:
			c['socket']['sockfilename'] = config.get('socket', 'sockfilename')
		except:
			pass
		try:
			c['socket']['port'] = config.get('socket', 'port')
		except:
			pass
		return c
	

