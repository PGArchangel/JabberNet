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
	
	
	def parseMessage(self,s,ptype):
		if ( s != None ):
			re_mess=re.compile(r"^%([^ ]+) ([^ ]+) ?(.*?)$")
			try:
				ss=re_mess.findall(s)
				plugin_name=ss[0][0]
				command_name=ss[0][1]
				query=ss[0][2]
				query_l=re.compile(r"([^ =\r\n]+)=([^ \r\n]*)").findall(ss[0][2]);
				query={}
				for a in query_l:
					query[a[0]]=a[1]
				print query
			except:
				return None
			if (plugin_name in config.plugins[ptype].keys()):
				unit=config.getDynamicPlugin(ptype,plugin_name)
				return config.execPluginFunction(unit,command_name,query)


	def message(self, conn,mess):
	#	print mess.getBody()
		s=mess.getBody()
		print s
		out=self.parseMessage(s,'commands')
		if ( out != None ):
			self.bot.send(xmpp.Message('pgarchangel@jabber.ru',out))
		
	def run(self):
		while self.bot.online:
			try:
				print 'bot.Process(1)'
				self.bot.Process(1)
				self.socketProcess()
			except KeyboardInterrupt:
				self.socketDisconnect()
				self.bot.disconnect()
				break

	def socketInit(self):
 		self.serversocket=socket.socket(socket.AF_UNIX)
		if ('port' in self.conf['socket'].keys()):
			self.serversocket.bind(('',self.conf['socket']['port']))
		else:
			try:
				if os.path.exists(self.conf['socket']['sockfilename']):
					os.unlink(self.conf['socket']['sockfilename'])
			except:
				raise 'error'
			self.serversocket.bind(self.conf['socket']['sockfilename'])
		self.serversocket.setblocking(0)
		self.serversocket.listen(1)
		self.rsocks = []
		self.wsocks = []
		self.rsocks.append(self.serversocket)
		self.senders = {}
	
	def socketDisconnect(self):
		self.rsocks=[]
		self.serversocket.close()
		try:
			os.unlink(self.conf['socket']['sockfilename'])
		except:
			pass
	
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
				client, name = sock.accept()
				self.rsocks.append(client)
			else:
				s = sock.recv(1024)
				print s
				if ( re.search('^exit',s) ):
					print 'exiting..'
					self.rsocks.remove(sock)
				else:
					out=self.parseMessage(s,'socket')
					if ( out != None ):
						try:
							sock.send(out)
						except:
							self.rsocks.remove(sock)

 

daemon = daemon()

daemon.run()


