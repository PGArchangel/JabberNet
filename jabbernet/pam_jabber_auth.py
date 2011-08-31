#!/usr/bin/python

import sys,os,xmpp,time,re,subprocess


jid = xmpp.JID(sys.argv[1])
bot = xmpp.Client(jid.getDomain(),debug=[])

conres=bot.connect()

if not conres:
	print "Unable to connect to server %s!"%(jid.getDomain())
	sys.exit(1)


authres=bot.auth(jid.getNode(),sys.argv[2],jid.getResource())
res=0
if not authres:
	res=1
if authres<>'sasl':
	print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server

bot.disconnect()

sys.exit(res)

