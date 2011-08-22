#!/usr/bin/python

import sys,os,xmpp,time,re,subprocess,json

import config

import socket
import select


#units=__import__('units')

#sys.path.append('units')

class daemon():
	def __init__(self):
		self._lastId=0
		self.queue = {'socket':{},'commands':{}}
		self.cfg = config.configurator(self)
		self.conf = self.cfg.conf
		self.jid = xmpp.JID(self.conf['jid'])
		self.bot = xmpp.Client(self.jid.getDomain(),debug=[])

		
		self.socketInit()
		self.jabberInit()
		
		self.clients={}
		self.clients['jabber']={}
		config.d=self
		
	def jabberInit(self):
		conres=self.bot.connect()
		self.jconnected=0
		if not conres:
			print "Unable to connect to server %s!"%(self.jid.getDomain())
#			sys.exit(1)
		else:
			authres=self.bot.auth(self.jid.getNode(),self.conf['password'],self.jid.getResource())
			if not authres:
				print "Unable to authorize on %s - check login/password."%(self.jid.getDomain())
			else:
				self.jconnected=1
#				sys.exit(1)
			if authres<>'sasl':
				print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
		self.bot.online = self.jconnected
		if (self.jconnected):
			self.bot.RegisterHandler('message',self.message)
			self.bot.sendInitPresence()
			return 1
		else:
			return 0
		
	def genId(self):
		return 'jabbernet_'+str(++self._lastId)
	
	def addToQueue(self,protocol,jfrom,mid,func,data):
		self.queue[protocol][jfrom][mid]={'run':func,'data':data}
	
	def packData(self,data):
		s=''
		for k in data:
			if (s!=''):
				s+=' '
			s+=k+'='+str(data[k])
		return s;
	
	def parseMessage(self,mess,ptype):
		if (type(mess) is str):
			s=mess
		else:
			s=mess.getBody()
		if ( s != None ):
			if (s[0]=='%'):
				re_mess=re.compile(r"^%([^ ]+) *([^ ]+) *?(.*?)$")
				try:
					ss=re_mess.findall(s)
					plugin_name=ss[0][0]
					command_name=ss[0][1]
					query=ss[0][2]
					query_l=re.compile(r"([^ =\r\n]+)=([^ \r\n]*)").findall(ss[0][2])
					query={}
					for a in query_l:
						query[a[0]]=a[1]
					print query
				except:
					return None
				if (plugin_name in self.cfg.plugins[ptype].keys()):
					unit=self.cfg.getDynamicPlugin(ptype,plugin_name)
					return self.cfg.execPluginFunction(unit,command_name,s,query)
			elif (s[0]=='@'):
				pass
				

	def sendMessage(self,command,data,to):
		out='';
		if (type(data) is types.DictType):
			out=self.PackData(data)
		mess=xmpp.Message(command+to,out)
		self.bot.send(mess)

	def message(self,conn,mess):
	#	print mess.getBody()
		s=mess.getBody()
		print s
		out=self.parseMessage(mess,'commands')
		if (type(out)==str):
			out=xmpp.Message(mess.getFrom(),out)
		if ( out != None ):
			self.bot.send(out)
		
	def run(self):
		self.jinit_c=0
		while 1:
			try:
				if (self.jconnected):
					print 'bot.Process(1)'
					self.bot.Process(1)
				else:
					if (self.jinit_c>10):
						print 'Try connect to jabber again...'
						self.jabberInit()
						self.jinit_c=0
					else:
						self.jinit_c+=1
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
		return 1
	
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


