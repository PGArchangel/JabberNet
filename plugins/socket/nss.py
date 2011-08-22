#!/usr/bin/python

class nss_plugin():
	def __init__(self,configurator,daemon):
		self.allowed=['getUser']

	def getUser(self,mess,a):
		print a
		if (((a.has_key('name'))and(a['name']=='stud'))or(not(a.has_key('name')))and(((a.has_key('uid'))and(a['uid']=='1004'))or(not(a.has_key('uid'))))):
			return '1\nstud\n1004\nx\n1004\nA student...\n/home/stud\n/bin/bash\n'
		else:
			return '0\n'
#	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
#	proc.wait()
#	return proc.stdout.readlines()
	
	
p=None
