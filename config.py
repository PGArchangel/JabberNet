#!/usr/bin/python

import os

def loadUnitsList(d):
	units={}
	for unit in os.listdir('plugins/'+d+'/'):
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
	sockfilename = config.get('socket', 'sockfilename')
	return {'jid':jid,'password':password,'socket':{'sockfilename':sockfilename,'port':int(config.get('socket', 'port'))}}
	
conf = loadConfig('config.ini')

plugins={}
plugins['commands']=loadUnitsList('commands')
plugins['socket']=loadUnitsList('socket')
