'''
	simple udp socket server
'''

import socket
import sys
from check import ip_checksum

HOST="" #Symbolic name meaing all available interferfaces
PORT=7878 #Arbitrary non-privileged port

def nextstatus(status):
	if (status == 'a'):
		return 'b'
	else:
		return 'a'

#Datagram (udp) socket
try:
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg:
	print 'Failed to create socket. Error Code: '+ str(msg[0])+' Message '+msg[1]
	sys.exit()

#Bind socket to local host and port
try:
	s.bind((HOST,PORT))
except socket.error, msg:
	print 'Bind failed. Error Code :'+str(msg[0])+' Message '+msg[1]
	sys.exit()

print 'Socket bind complete'
status='a'

#now keep talking with client
while 1:
	print
	#receive data from client(data,addr)
	d=s.recvfrom(1024)
	data=d[0]
	addr=d[1]
	rc_status=data[0]
	get_checksum=data[1:3]
	rc_msg=data[3:]
	if not rc_msg:
		break
	reply_msg='OK...' +rc_msg
	if ( rc_status==status and get_checksum==ip_checksum(rc_msg) ):
		snd_status=rc_status
		snd_checksum=ip_checksum(reply_msg)
		reply=snd_status+snd_checksum+reply_msg
		s.sendto(reply,addr)
		print 'Message['+addr[0]+':'+str(addr[1])+']-'+rc_msg
		status=nextstatus(status)
	else:
		s.sendto(reply,addr)
		print 'Message['+addr[0]+':'+str(addr[1])+']-'+rc_msg


s.close()

