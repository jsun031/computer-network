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
def basecheck(base, cwnd, rc_seqnum):#as base and seq is between 0 to 9
        if(base%10+cwnd<10):
                if (base%10<=rc_seqnum and rc_seqnum<base%10+cwnd ):
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
ACKset=['','','','']

while(1):
	input_msg=raw_input('Enter message to send : ')

	try :
		length=2
		begin=0
		end=2
		while(len(input_msg[0:]) <base or len(input_msg[begin:])>0 ):
			while(len(input_msg[begin:])>0 and nextseqnum<base+cwnd):
				if not (nextseqnum in ACKset):
					snd_msg=input_msg[begin:end]
					d=ip_checksum(snd_msg)
					snd_seqnum=str(nextseqnum % 10)
					send_msg=snd_seqnum+d+snd_msg
					s.sendto(send_msg,(host,port))

					print 'Send message : '+snd_msg+', sndseqnum :' +snd_seqnum
				nextseqnum=nextseqnum+1
				#print 'nexdtseqnum is '+str(nextseqnum)+', base+cwnd is '+str(base+cwnd)
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
				addr=d[1]
				rc_seqnum=int(reply[0])
				get_checksum=reply[1:3]
				reply_msg=reply[3:]
				print 'Server reply : '+reply_msg+ ', rc_seqnum is '+ str(rc_seqnum)

				if(get_checksum==ip_checksum(reply_msg)):
					dst=dst_base_rc(base,cwnd,rc_seqnum)
					print 'dst'+str( dst)+', base'+ str(base)
					ACKset[dst]=1
					while (ACKset and ACKset[0]):
						base=(base+1)%10
						#ACKset.pop([0])
						del ACKset[0]
						ACKset.append('')

			if(out=='T'):
				nextseqnum=base
				begin=nextseqnum*length
                                if(len(input_msg[nextseqnum*length:])<length):
                                        end=begin+len(input_msg[nextseqnum*length:])
                                else:
                                        end=(nextseqnum+1)*length

			
			print 'My nexseqnum is '+ str(nextseqnum)+', base : ' +str(base)
			

	except socket.error, msg:
		print 'Error Code : ' +str(msg[0])+' Message '+msg[1]
		sys.exit()
