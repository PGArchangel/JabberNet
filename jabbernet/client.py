#!/usr/bin/python

import sys, socket, time
 
class Client:
	def __init__(self, 
		sockfile='./bot.sock',
		buffersize=1024,
		testmode=0):

		self.sockfile = sockfile
		self.buffersize = buffersize
		self.testmode = testmode

		self.socket = socket.socket(socket.AF_UNIX)
		self.socket.connect(self.sockfile)
		self.socket.send('%nss getUser stud\r')
#		print self.socket.recv(1024)
		self.socket.close()


        
c=Client()

