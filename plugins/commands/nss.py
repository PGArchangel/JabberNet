#!/usr/bin/python

import pwd,xmpp

class nss_plugin():
	def __init__(self,configurator,daemon):
		self.cfg=configurator
		self.d=daemon
		self.allowed=['getUser']

	#def _firstUser():
	

	#def _nextUser():
	
	#def _closeUsers():


	
	def getUser(self,mess,a): # %nss getUser uid=1000 name=stud
		try:
			if (a.has_key('uid')):
				p=pwd.getpwuid(a['uid'])
			elif (a.has_key('name')):
				p=pwd.getpwnam(a['name'])
			else:
				p=None
		except:
			p=None
		if (p!=None):
			s='@'+mess.getID()+'\n'+self.d.packData({'pw_name':p.pw_name, 'pw_passwd':p.pw_passwd, 'pw_uid':p.pw_uid, 'pw_gid':p.pw_gid, 'pw_gecos':p.pw_gecos, 'pw_dir':p.pw_dir, 'pw_shell':p.pw_shell})
			out=xmpp.Message(mess.getFrom(),s)
			mid=self.d.genId()
			out.setID(mid)
			return s
		
	#	proc=subprocess.Popen("getent passwd "+a['name']+' '+a['uid'],shell=True,stdout=subprocess.PIPE)

	#	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
	#	proc.wait()
	#	return proc.stdout.readlines()
	
p=None
