#!/usr/bin/python

import sys,os,xmpp,time,re,subprocess

import config

sys.path.append('units')

conf=config.conf
def parseMessage(s):
	if ( s != None ):
		re_mess=re.compile(r"([^ ]+)")
		ss=re_mess.findall(s)
		print ss;
		if (ss[0] in config.units):
			unit=__import__(''+ss[0])
			if (ss[1] in unit.allowed):
				plugin = getattr(unit,ss[1])
				return plugin(ss[2:])




jid = xmpp.JID(conf['jid'])
bot = xmpp.Client(jid.getDomain(),debug=[])

conres=bot.connect()

if not conres:
	print "Unable to connect to server %s!"%server
	sys.exit(1)


authres=bot.auth(jid.getNode(),conf['password'],jid.getResource())
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
	print s
	out=parseMessage(s)
	bot.send(xmpp.Message('pgarchangel@jabber.ru',out))

bot.RegisterHandler('message',message)


bot.sendInitPresence()

#bot.send(xmpp.Message('pgarchangel@jabber.ru','hello'))

while bot.online:
	try:
		bot.Process(1)
	except KeyboardInterrupt:
		bot.disconnect()
		break


