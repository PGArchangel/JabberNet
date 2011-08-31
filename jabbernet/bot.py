#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		i='jabbernet_'+str(self._lastId)
		self._lastId+=1
		return i
	
	def addToQueue(self,protocol,jfrom,mid,func,data):
		self.queue[protocol][jfrom][mid]={'run':func,'data':data}
	
	def packData(self,data,format='list'):
		s=''
		if (format=='list'):
			print data
			for k in data:
				if (s!=''):
					s+=' '
				s+=k+'='+str(data[k])
		elif (format=='json'):
			s=json.dumps(data)
		return format+':'+s;
	
	def unpackData(self,s,format='list'):
		data=None
		print s
		f=re.search('^([\w\d_]+):(.*)',s)
		if (f!=None):
			format=f.group(1)
			s=f.group(2)
		if (format=='list'):
			data_l=re.compile(r"([^ =\r\n]+)=([^ \r\n]*)").findall(s)
			data={}
			for a in data_l:
				data[a[0]]=a[1]
		elif (format=='json'):
			data=json.loads(s)
		return data
						
	def parseMessage(self,mess,ptype=None):
		s=''
		if (ptype==None):
			if (type(mess) is str):
				ptype='other'
			elif (isinstance(mess,xmpp.Message)):
				ptype='commands'
			elif (isinstance(mess,config.socketMessage)):
				ptype='socket'
			
		if (ptype=='other'):
			s=mess
		elif (ptype=='commands'):
			s=mess.getBody()
		elif (ptype=='socket'):
			s=mess.getBody()
		elif (ptype=='localsocket'):
			s=mess.getBody()
			
			
		if (( s != None ) and (s!='')):
			if (s[0]=='%'):
				re_mess=re.compile(r"^%([^ \r\n]+) *([^ ]*) *(.*?)$")
				try:
					ss=re_mess.findall(s)
					plugin_name=ss[0][0]
					command_name=ss[0][1]
					query=ss[0][2]
					query=self.unpackData(query)
				except:
					print "Can't parse message's data..."
					return None
				print "Loading "+plugin_name+" plugin..."
				if (plugin_name in self.cfg.plugins[ptype].keys()):
					print "Plugin found..."
					unit=self.cfg.getDynamicPlugin(ptype,plugin_name)
					return self.cfg.execPluginFunction(unit,command_name,mess,query)
			elif (s[0]=='@'):
#				try:
					print "Answer found... "
					ss=re.compile(r"^@([\d\w_]+)[\n\r]{1,2}(.+)").search(s)
					print "Checking answer..."
					print ss.group(1)
					print self.queue
					print self.queue['commands'][ss.group(1)]
					if (ss.group(1) in self.queue['commands']):
						print "Executing OnAnswer: "+ss.group(1)+' from '
						data=self.unpackData(ss.group(2))
						print data
						print "Answers' data:"
						print data
						self.queue['commands'][ss.group(1)]['onanswer'](mess,data,self.queue['commands'][ss.group(1)]['data'])
						del self.queue['commands'][ss.group(1)]
#				except:
#					pass
				

	def sendMessage(self,mess,onanswer=None):
		self.activity=4+self.activity*0.3
		out='';
		if (isinstance(mess,xmpp.Message)):
			mid=self.genId()
			mess.setID(mid)
			if (onanswer):
				print "OnAnswer event registered: "+mid+' to '
				self.queue['commands'][mid]={'onanswer':onanswer,'data':None}
			print "Sending jabber message: "+mess.getBody()
			self.bot.send(mess)
		elif (isinstance(mess,config.socketMessage)):
			print "Sending socket message: "+mess.getBody()
			mess.send()
		return 1

	def message(self,conn,mess):
	#	print mess.getBody()
		s=mess.getBody()
		print "Message received: "+s
		print "Sender: "
		self.activity+=4+self.activity*0.1
		print mess.getFrom()
		out=self.parseMessage(mess,'commands')
		if (type(out)==str):
			out=xmpp.Message(mess.getFrom(),out)
		elif ( isinstance(out,xmpp.Message) ):
			self.bot.send(out)
		
	def run(self):
		self.jinit_c=0
		self.sleep_time=1.0
		self.activity=1
		while 1:
			try:
				if (self.jconnected):
					print 'bot.Process(1)'
					self.bot.Process(self.sleep_time)
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
			self.sleep_time=1/float(self.activity)
			self.activity=self.activity-1
			if (self.activity<1):
				self.activity=1
			if (self.activity>1000):
				self.activity=1000
			print "Время ожидания: %f"%self.sleep_time
			print "Активность приложения:"
			print self.activity

	def socketInit(self):
		self.rsocks = []
		self.wsocks = []
		if ('port' in self.conf['socket'].keys()):
	 		self.serversocket=socket.socket(socket.AF_INET)
			self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.serversocket.bind(('',self.conf['socket']['port']))
			self.serversocket.setblocking(0)
			self.serversocket.listen(5)
			self.rsocks.append(self.serversocket)
		if ('sockfilename' in self.conf['socket'].keys()):
			try:
				if os.path.exists(self.conf['socket']['sockfilename']):
					os.unlink(self.conf['socket']['sockfilename'])
			except:
				raise 'error'
	 		self.localsocket=socket.socket(socket.AF_UNIX)
			self.localsocket.bind(self.conf['socket']['sockfilename'])
			self.localsocket.setblocking(0)
			self.localsocket.listen(5)
			self.rsocks.append(self.localsocket)

		self.senders = {}
		return 1
	
	def socketDisconnect(self):
		self.rsocks=[]
		self.serversocket.close()
		self.localsocket.close()
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
				self.senders[client]='socket'
				self.activity+=20
			elif sock == self.localsocket:
				client, name = sock.accept()
				self.rsocks.append(client)
				self.senders[client]='localsocket'
				self.activity+=20			
			else:
				ptype=self.senders[sock]
				print ptype
				print ""
				s = sock.recv(1024)
				print "Socket message received: "+s
				if (re.match(r"^[ \t\r\n]+$",s)):
					self.rsocks.remove(sock)
					del self.senders[sock]
				else:					
					mess=config.socketMessage(s,sock)
					if (( re.search('^exit',s) ) or (s=="")):
						print 'exiting..'
						self.rsocks.remove(sock)
						del self.senders[sock]
					else:
						self.activity=self.activity+4+self.activity*0.1
						out=self.parseMessage(mess,ptype)
						if ( out != None ):
							try:
								print "Sending answer on socket message..."
								s=out
								if (isinstance(out,config.socketMessage)):
									s=out.getBody()
								sock.send(s)
							except:
								self.rsocks.remove(sock)
								del self.senders[sock]

 

daemon = daemon()

daemon.run()


