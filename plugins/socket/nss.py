#!/usr/bin/python


allowed=['getUser']

def getUser(a):
	print a
	if (a['name']=='stud')and(a['uid']=='1004'):
		return 'stud\n1004\nx\n1004\nA student...\n/home/stud\n/bin/bash\n'
	return a[0];
#	proc=subprocess.Popen("ssh root@"+ip+" 'echo dfdf11>/data/test;exit;';echo '111';",shell=True,stdout=subprocess.PIPE)
#	proc.wait()
#	return proc.stdout.readlines()
	
