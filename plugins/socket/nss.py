#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import xmpp
import types

class nss_plugin():
	def __init__(self,configurator,daemon):
		self.cfg=configurator
		self.d=daemon
		self.allowed={ 'getUser':{},  'toFirstUser':{}, 'getShadow':{} }
		self.cachedUsers=[]
		self.currentUser=None
		
	def getNextUser(self): # Возвращает следующего пользователя из кеша
		if (self.currentUser>len(self.cachedUsers)-1):
			return None
		user=self.cachedUsers[self.currentUser]
		self.currentUser+=1
		return user

	def cachedUsersList(self,data):
		""" Заносит список пользователей из data в кеш """
		self.cachedUsers=data['users']
		if (len(self.cachedUsers)>0):
			self.currentUser=0
			return 1
		else:
			self.currentUser=None
			return 0

	def toFirstUser(self,mess,a):
		print "Going to first user..."
		jm=xmpp.Message('admin@localhost','%nss getUsersList')
	
		onanswer=lambda message,answer,data: ( self.cachedUsersList(answer) and self.d.sendMessage(config.socketMessage('1\n',mess.socket)) or self.d.sendMessage(config.socketMessage('0\n',mess.socket)) )
		self.d.sendMessage(jm,onanswer)
		
	def userToString(self,user):
		return user['pw_name']+'\n'+str(user['pw_uid'])+'\n'+user['pw_passwd']+'\n'+str(user['pw_gid'])+'\n'+user['pw_gecos']+'\n'+user['pw_dir']+'\n'+user['pw_shell']+'\n'
		
	def shadowToString(self,user):
		return user['sp_namp']+'\n'+user['sp_pwdp']+'\n'+str(user['sp_lstchg'])+'\n'+str(user['sp_min'])+'\n'+str(user['sp_max'])+'\n'+str(user['sp_warn'])+'\n'+str(user['sp_inact'])+'\n'+str(user['sp_expire'])+'\n'+str(user['sp_flag'])+'\n'
		
	def getShadow(self,mess,a):
		if (a.has_key('sp_namp')):
			jm=xmpp.Message('admin@localhost','%nss getShadow '+self.d.packData(a))
			onanswer=lambda message,answer,data: ( isinstance(answer,types.DictType) and answer.has_key('sp_namp') and self.d.sendMessage(config.socketMessage('1\n'+self.shadowToString(answer),mess.socket)) or self.d.sendMessage(config.socketMessage('0\n',mess.socket)) )
			
			self.d.sendMessage(jm,onanswer)
		
	def getUser(self,mess,a):
	
		if ((a.has_key('pw_name')) or (a.has_key('pw_uid'))):
			jm=xmpp.Message('admin@localhost','%nss getUser '+self.d.packData(a))

			onanswer=lambda message,answer,data: ( isinstance(answer,types.DictType) and answer.has_key('pw_name') and self.d.sendMessage(config.socketMessage('1\n'+self.userToString(answer),mess.socket)) or self.d.sendMessage(config.socketMessage('0\n',mess.socket)) )

			self.d.sendMessage(jm,onanswer)
			
			return None
		else:
			s=''
			print "Getting next user..."
			if (len(self.cachedUsers)>0):
				print "!!"
				user=self.getNextUser()
				print user
				if (user!=None):
					s='1\n'+self.userToString(user)
				else:
					s='0\n'
			else:
				s='0\n'
			print s
			return s
#	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
#	proc.wait()
#	return proc.stdout.readlines()
	
	
p=None
