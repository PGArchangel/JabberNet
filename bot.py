#!/usr/bin/python

import sys,os,xmpp,time,re,subprocess,json

import config

import socket
import select


#units=__import__('units')

#sys.path.append('units')

class daemon():
	def __init__(self):
		self.conf = config.conf
		self.jid = xmpp.JID(self.conf['jid'])
		self.bot = xmpp.Client(self.jid.getDomain(),debug=[])
		conres=self.bot.connect()
		if not conres:
			print "Unable to connect to server %s!"%(self.jid.getDomain())
			sys.exit(1)
		authres=self.bot.auth(self.jid.getNode(),self.conf['password'],self.jid.getResource())
		if not authres:
			print "Unable to authorize on %s - check login/password."%(self.jid.getDomain())
			sys.exit(1)
		if authres<>'sasl':
			print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
		self.bot.online = 1
		self.bot.RegisterHandler('message',self.message)
		self.bot.sendInitPresence()
		
		self.socketInit()
	
	
	def parseMessage(self,s):
		if ( s != None ):
			re_mess=re.compile(r"^%([^ ]+) ([^ ]+) ?(.*)$")
			try:
				ss=re_mess.findall(s)
				plugin_name=ss[0][0]
				command_name=ss[0][1]
				query=ss[0][2:]
			except:
				return None
			if (plugin_name in config.plugins['commands'].keys()):
				unit=config.loadDynamicPlugin('commands',plugin_name)
				if (command_name in unit.allowed):
					command = getattr(unit,command_name)
					return command(query)


	def message(self, conn,mess):
	#	print mess.getBody()
		s=mess.getBody()
		print s
		out=self.parseMessage(s)
		self.bot.send(xmpp.Message('pgarchangel@jabber.ru',out))
		
	def run(self):
		while self.bot.online:
			try:
				print 'bot.Process(1)'
				self.bot.Process(1)
				self.socketProcess()
			except KeyboardInterrupt:
				self.bot.disconnect()
				break

	def socketInit(self):
		self.serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if (self.conf['socket']['port']):
			self.serversocket.bind(('',self.conf['socket']['port']))
		else:
			self.serversocket.bind(self.conf['sockfilename'])
		self.serversocket.setblocking(0);
		self.serversocket.listen(1)
		self.rsocks = []
		self.wsocks = []
		self.rsocks.append(self.serversocket)
		self.senders = {}
	
	def socketProcess(self):
		print 'Checking'
		try:
			reads, writes, errs = select.select(self.rsocks, self.wsocks, [], 0)
			print 'Checking tried...'
		except:
			print 'Except...'
			return
		for sock in reads:
			if sock == self.serversocket:
				print sock
				client, name = sock.accept()
				self.rsocks.append(client)
			elif not `sock` in self.senders.keys():
				plugin_name = sock.recv(1024)
				print plugin_name
#				if (plugin_name in config.plugins['socket']):
					
			else:
				message = sock.recv(1024)
				sock.send('Message OK')
				print message
				self.rsocks.remove(sock)
				del self.senders[`sock`]
 

daemon = daemon()

daemon.run()


