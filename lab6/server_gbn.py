'''
	simple udp socket server
'''

import socket
import sys
from check import ip_checksum

HOST="" #Symbolic name meaing all available interferfaces
PORT=7878 #Arbitrary non-privileged port

#def nextstatus(status):
#	if (status == 'a'):
#		return 'b'
#	else:
#		return 'a'

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

expectedseqnum=0

#now keep talking with client
while 1:
	print
	#receive data from client(data,addr)
	d=s.recvfrom(1024)
	data=d[0]
	addr=d[1]
	rc_seqnum=data[0]
	get_checksum=data[1:3]
	rc_msg=data[3:]


	print 'Message['+addr[0]+':'+str(addr[1])+']-'+rc_msg
	if ( rc_msg==''):
		status=0
		continue

	reply_msg='OK...' +rc_msg
	if ( rc_seqnum==str(expectedseqnum) and get_checksum==ip_checksum(rc_msg) ):
		expectedseqnum=(expectedseqnum+1)%10
		snd_seqnum=str(expectedseqnum)
		snd_checksum=ip_checksum(reply_msg)
		reply=rc_seqnum+snd_seqnum+snd_checksum+reply_msg
		s.sendto(reply,addr)
		print 'expected number is '+str(expectedseqnum)
	else:
		snd_seqnum=str(expectedseqnum)
		snd_checksum=ip_checksum('')
		if expectedseqnum==0:
			ACK=9
		else:
			ACK=expectedseqnum-1
		reply=str(ACK)+snd_seqnum+snd_checksum+''
		s.sendto(reply,addr)
		print 'expected number is '+str(expectedseqnum)

s.close()

