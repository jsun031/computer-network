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

def basecheck(base, cwnd, rc_seqnum):#as base and seq is between 0 to 9
	if ( base%10+cwnd < 10 ) :
        	if ( base%10 <= rc_seqnum and rc_seqnum < (base%10 +cwnd) ):
                	return True
		else:
			return False
        else:
                if(base%10<=rc_seqnum ):
                      	return True
                else:
                       	if(rc_seqnum<(base%10+cwnd)%10):
				return True
			else:
				return False
def dst_base_rc(base,cwnd,rc_seqnum):
	if(base%10+cwnd<10):
		return rc_seqnum-base
	else:
		if(base%10<=rc_seqnum):
			return rc_seqnum-base
		else:#rc_seqnum<base
			return rc_seqnum+10-base

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
ACK=0
tmp_msg=[0, 0,0 ,0]
tmp_ACK=[0, 0, 0, 0]

cwnd=4
base=0

#now keep talking with client
while 1:
	#receive data from client(data,addr)
	d=s.recvfrom(1024)
	data=d[0]
	addr=d[1]
	rc_seqnum=data[0]
	rc=int(rc_seqnum)
	get_checksum=data[1:3]
	rc_msg=data[3:]

	print 'Message['+addr[0]+':'+str(addr[1])+']-'+rc_msg
	if ( rc_msg==''):
		status=0
		continue
	
	if(get_checksum==ip_checksum(rc_msg) ):#ignore wrong msg
		if (basecheck(base,cwnd,rc)):
			ACK=rc_seqnum#1 digit
			reply_msg='OK...' +rc_msg
			snd_checksum=ip_checksum(reply_msg)#2 digits
			reply=ACK+snd_checksum+reply_msg
			s.sendto(reply,addr)
			print 'msg within current window, '+' ACK is '+ACK

			dst=dst_base_rc(base,cwnd,rc)
			print 'dst' + str(dst)
			tmp_ACK[dst]=1
			tmp_msg[dst]=rc_msg
			while (tmp_ACK and tmp_ACK[0]):
				print 'deliver msg: '+ tmp_msg[0]
				#tmp_ACK.pop(0)
				#tmp_msg.pop(0)
				del tmp_ACK[0]
				del tmp_msg[0]
				tmp_ACK.append('')
				tmp_msg.append('')
				base=(base+1)%10

		
			#base=base-base%10+rcseqnum+1
		else:
			if basecheck(base-cwnd,cwnd,rc):
				ACK=base
				reply_msg='OK...' +rc_msg
				snd_checksum=ip_checksum('')
				reply=ACK+snd_checksum+''
				s.sendto(reply,addr)
				print 'msg is within last window,'+' ACK is '+ACK


s.close()

