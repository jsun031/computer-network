''' 
	udp socket client
	Silver Moon
'''

import socket #for sockets
import sys #for exit
import select
from check import ip_checksum
from time import sleep
#def nextstatus(status):
#	if(status=='a'):
#		return 'b'
#	else:
#		return 'a'

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
cwnd=4
base=0
nextseqnum=0
while(1):
	input_msg=raw_input('Enter message to send : ')

	try :
		length=2
		begin=0
		end=2
		while(len(input_msg[0:]) <base or len(input_msg[begin:])>0 ):
			while(len(input_msg[begin:])>0 and nextseqnum<base+cwnd):
				snd_msg=input_msg[begin:end]
				d=ip_checksum(snd_msg)
				snd_seqnum=str(nextseqnum % 10)
				send_msg=snd_seqnum+d+snd_msg
				s.sendto(send_msg,(host,port))

				print 'Send message : '+snd_msg+', sndseqnum :' +snd_seqnum
				nextseqnum=nextseqnum+1
				print 'nextseqnum is '+str(nextseqnum)+', base+cwnd is '+str(base+cwnd)
				sleep(1)
				begin=nextseqnum*length
				if(len(input_msg[nextseqnum*length:])<length):
					end=begin+len(input_msg[nextseqnum*length:])
				else:
					end=(nextseqnum+1)*length


			readable,writable,exceptional=select.select(inputs,outputs,inputs,timeout)
			out='T'
			for s in readable:
				out='F'
				#receive data from client (data, addr)
				d=s.recvfrom(1024)
				reply=d[0]
				exp=d[1]
				rc_seqnum=int(reply[0])
				get_checksum=reply[2:4]
				reply_msg=reply[4:]
				print 'Server reply : '+reply_msg+ ', rc_seqnum is '+ str(rc_seqnum)

				if(get_checksum==ip_checksum(reply_msg)):	
					if(base%10+cwnd<10):
						if (base%10<=rc_seqnum and rc_seqnum<base%10+cwnd ):
							base=base-(base%10)+rc_seqnum+1
					else:
						if(base%10<=rc_seqnum ):
							base=base-(base%10)+rc_seqnum+1
						else:
							if(rc_seqnum<=(base%10+cwnd)%10):
								base=base-base%10+rcseqnum+1

			if(out=='T'):
				nextseqnum=base
			
			print 'My nexseqnum is '+ str(nextseqnum)+', base : ' +str(base)
			

	except socket.error, msg:
		print 'Error Code : ' +str(msg[0])+' Message '+msg[1]
		sys.exit()
