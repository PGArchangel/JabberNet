#!/usr/bin/python

import os

units=[]
def loadUnitsList():
	units=[]
	for unit in os.listdir('units/'):
		if unit.endswith('.py'):
			unit_name = unit[:-3]
			if (unit_name != '__init__'):
				units.append(unit_name)
	return units


def loadConfig(filename):
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read(filename)
	jid = config.get('connection', 'jid')
	password = config.get('connection', 'password')
	return {'jid':jid,'password':password}
	
conf = loadConfig('config.ini')


units=loadUnitsList()
