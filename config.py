#!/usr/bin/python

import os

def getDynamicPlugin(ptype,pname):
	if (plugins[ptype][pname]==None):
		unit=__import__('plugins.'+ptype+'.'+pname)
		unit=getattr(unit,ptype)
		unit=getattr(unit,pname)
		plugins[ptype][pname]=unit
	else:
		unit=plugins[ptype][pname]
	return unit
	
def execPluginFunction(unit,fname,query=None):
	if (fname in unit.allowed):
		command = getattr(unit,fname)
		return command(query)


def loadUnitsList(ptype):
	units={}
	for unit in os.listdir('plugins/'+ptype+'/'):
		if unit.endswith('.py'):
			unit_name = unit[:-3]
			if (unit_name != '__init__'):
				units[unit_name] = None
	return units


def loadConfig(filename):
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
	
conf = loadConfig('config.ini')

plugins={}
plugins['commands']=loadUnitsList('commands')
plugins['socket']=loadUnitsList('socket')
