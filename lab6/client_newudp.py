''' 
	udp socket client
	Silver Moon
'''

import socket #for sockets
import sys #for exit
import select
from check import ip_checksum

def nextstatus(status):
	if(status=='a'):
		return 'b'
	else:
		return 'a'

#create dgram udp socket
try:
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to creat socket'
	sys.exit()

host = 'localhost';
port=7878;

inputs=[s]
outputs=[]
timeout=10
while(1):
	input_msg=raw_input('Enter message to send : ')

	try :
		status='a'
		length=2

		while(len(input_msg)>0):
			#Set the whole string
			snd_msg=input_msg[0:length]
			print 'Send message : '+snd_msg
			d=ip_checksum(snd_msg)
			snd_status=status
			send_msg=snd_status+d+snd_msg
			s.sendto(send_msg,(host,port))

			readable,writable,exceptional=select.select(inputs,outputs,inputs,timeout)
			for s in readable:
				#receive data from client (data, addr)
				d=s.recvfrom(1024)
				reply=d[0]
				addr=d[1]
				rc_status=reply[0]
				get_checksum=reply[1:3]
				reply_msg=reply[3:]
	
				print 'Server reply : '+reply_msg
				print 'rc Status is '+ rc_status
				if (rc_status==status and get_checksum==ip_checksum(reply_msg)):
					input_msg=input_msg[length:]
					if(len(input_msg)<length):
						length=len(input_msg)
					status=nextstatus(status)


			print 'My Status is '+ status
	except socket.error, msg:
		print 'Error Code : ' +str(msg[0])+' Message '+msg[1]
		sys.exit()
