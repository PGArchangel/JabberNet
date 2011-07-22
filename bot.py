#!/usr/bin/python

import sys,os,xmpp,time,re,subprocess


def loadConfig(filename):
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read(filename)
	jid = config.get('connection', 'jid')
	password = config.get('connection', 'password')
	return {'jid':jid,'password':password}
	
config = loadConfig('config.ini');


jid = xmpp.JID(config['jid'])
bot = xmpp.Client(jid.getDomain(),debug=[])

conres=bot.connect()

if not conres:
	print "Unable to connect to server %s!"%server
	sys.exit(1)


authres=bot.auth(jid.getNode(),config['password'],jid.getResource())
if not authres:
	print "Unable to authorize on %s - check login/password."
	sys.exit(1)
if authres<>'sasl':
	print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server

bot.online = 1

def client_getProfile(ip):
	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
	proc.wait()
	return proc.stdout.readlines()

def message(conn,mess):
	global bot
#	print mess.getBody()
	s=mess.getBody()
	if ( s != None ):
		re_mess=re.compile(r"([^ ]+)")
		ss=re_mess.findall(s);
		if (ss[0]=='getProfile'):
			out=client_getProfile(ss[1]);
			for line in out:
				print line
			bot.send(xmpp.Message('pgarchangel@jabber.ru',out))

bot.RegisterHandler('message',message)

bot.send(xmpp.Message('pgarchangel@jabber.ru','hello'))

bot.sendInitPresence()

while bot.online:
	try:
		bot.Process(1)
	except KeyboardInterrupt:
		bot.disconnect()
		break


