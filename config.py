#!/usr/bin/python

import os

class configurator():
	def __init__(self,daemon=None):
		self.d=daemon
		self.conf = self.loadConfig('config.ini')

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
		if (fname in unit.p.allowed):
			command = getattr(unit.p,fname)
			return command(mess,query)


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
	

