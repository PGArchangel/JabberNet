#!/usr/bin/python

import pwd,spwd,xmpp

class nss_plugin():
	def __init__(self,configurator,daemon):
		self.cfg=configurator
		self.d=daemon
		self.allowed={ 'getUser':{}, 'getUsersList':{} , 'getShadow':{} }

	#def _firstUser():
	

	#def _nextUser():
	
	#def _closeUsers():
	def pwdStructToDict(self,p):
		if (isinstance(p,pwd.struct_passwd)):
			return {'pw_name':p.pw_name, 'pw_passwd':p.pw_passwd, 'pw_uid':p.pw_uid, 'pw_gid':p.pw_gid, 'pw_gecos':p.pw_gecos, 'pw_dir':p.pw_dir, 'pw_shell':p.pw_shell}
		else:
			return p
			
	def spwdStructToDict(self,s):
		if (isinstance(s,spwd.struct_spwd)):
			return {'sp_namp':s.sp_nam, 'sp_pwdp':s.sp_pwd, 'sp_lstchg':s.sp_lstchg, 'sp_min':s.sp_min, 'sp_max':s.sp_max, 'sp_warn':s.sp_warn, 'sp_inact':s.sp_inact, 'sp_expire':s.sp_expire, 'sp_flag':s.sp_flag}
		else:
			return s
		

	def getUsersList(self,mess,a):
		users=pwd.getpwall()
		i=0
		while (i<len(users)):
			users[i]=self.pwdStructToDict(users[i])
			i+=1
		data={}
		data['users']=users
		data['users'].append({'pw_name':'stud', 'pw_passwd':'x', 'pw_uid':'1004', 'pw_gid':'1004', 'pw_gecos':'student,,,', 'pw_dir':'/home/stud', 'pw_shell':'/bin/bash'})
		s='@'+mess.getID()+'\n'+self.d.packData(data,'json')
		out=xmpp.Message(mess.getFrom(),s)
		mid=self.d.genId()
		out.setID(mid)
		return out
		
		
	def getUser(self,mess,a): # %nss getUser uid=1000 name=stud
		s=''
		p=None
		print a
		try:
			if (a.has_key('pw_uid')):
				if (a['pw_uid']=='1004'):
					p={'pw_name':'stud', 'pw_passwd':'x', 'pw_uid':'1004', 'pw_gid':'1004', 'pw_gecos':'student,,,', 'pw_dir':'/home/stud', 'pw_shell':'/bin/bash'}
				else:
					p=pwd.getpwuid(a['pw_uid'])
			elif (a.has_key('pw_name')):
				if (a['pw_name']=='stud'):
					p={'pw_name':'stud', 'pw_passwd':'x', 'pw_uid':'1004', 'pw_gid':'1004', 'pw_gecos':'student,,,', 'pw_dir':'/home/stud', 'pw_shell':'/bin/bash'}
				else:
					p=pwd.getpwnam(a['pw_name'])
			else:
				users=pwd.getpwall()
				i=0
				while (i<len(users)):
					users[i]=self.pwdStructToDict(users[i])
					i+=1
				s='@'+mess.getID()+'\n'+self.d.packData(users,'json')
		except:
			p=None
		if (s==''):
			if (p!=None):
				s='@'+mess.getID()+'\n'+self.d.packData(self.pwdStructToDict(p))
			else:
				s='@'+mess.getID()+'\n'+'success=false'
		out=xmpp.Message(mess.getFrom(),s)
		mid=self.d.genId()
		out.setID(mid)
		return out
		
	
	def getShadow(self,mess,a):
		if a.has_key('sp_namp'):
			print a
			try:
				if (a['sp_namp']=='stud'):
					shadow={'sp_namp':'stud', 'sp_pwdp':'$6$6MxIEDSq$0nenscxg5NOTaPIwi1tv4rE3zx2h0P55ANwpf7UUYp85ADMZDpKk3N/a/qk2GPrrcDtbBqFI3kC6rkDzM/ZZI.', 'sp_lstchg':15155, 'sp_min':0, 'sp_max':99999, 'sp_warn':7, 'sp_inact':-1, 'sp_expire':-1, 'sp_flag':-1}
				else:
					shadow=spwd.getspnam(a['sp_namp'])
			except:
				shadow=None
			if (shadow!=None):
				shadow=self.spwdStructToDict(shadow)
				s='@'+mess.getID()+'\n'+self.d.packData(self.spwdStructToDict(shadow))
			else:
				s='@'+mess.getID()+'\n'+'success=false'
		out=xmpp.Message(mess.getFrom(),s)
		mid=self.d.genId()
		out.setID(mid)
		return out			
				
	
	#	proc=subprocess.Popen("getent passwd "+a['name']+' '+a['uid'],shell=True,stdout=subprocess.PIPE)

	#	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
	#	proc.wait()
	#	return proc.stdout.readlines()
	
p=None
