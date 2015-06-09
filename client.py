import socket #for sockets
import sys #for exit
import re
import select
import getpass
def listening(rc_msg):
	show=''
	od=1
	print ' a new message: '
	for a in rc_msg[1:]:
		if(a!='/' and a!='^' and a!='&' ):
			show=show+str(a)
		elif(a=='^'):
			show=(show)+' from '
		elif(a=='&'):
			show=show+' hashtag: '
		elif(a=='/'):
			print str(od)+':'+show
			show=''
			od=od+1

		
def main_menu(status,s,unread_msg):
	#inputs=[s]
	#outputs=[]
	#timeout=1
	#readable,writable,exceptional=select.select(inputs,outputs,inputs,timeout)
        #for s in readable:
	#	#receive data from client (data, addr)
        #        rc=s.recvfrom(1024)
	#	while(int(rc[0])==4):
	#		rc_msg= s.recv(1024)
	#		print 'message:'	
	#		show=''
	#		od=1
	#		for a in rc_msg[2:]:
	#		if(a!='/' and a!='^' and a!='&' ):
	#			show=show+str(a)
	#		elif(a=='^'):
	#			show=(show)+' from '
	#		elif(a=='&'):
	#			show=show+' hashtag: '
	#		elif(a=='/'):
	#			print str(od)+':'+show
	#			show=''
	#			od=od+1
	num=int(raw_input('main menu:\n1. see messages\n2. edit followee\n3. post a message\n4. hashtag search\n5. see follower\n6. logout\n'))
	#listening(s)
        if (num==1):
                msg=offline_msg(s,unread_msg)
        elif (num==2):
                msg=edit_sub(s)
        elif (num==3):
                msg=post_msg(s)
        elif (num==4):
                msg=hashtag_search(s)
        elif (num==5):
                see_follower(s)
        elif (num==6):
		s.sendall(str(0))
                sys.exit(0)
	else :
		print 'Please input a number between 1 and 4';
		main_menu(status,s,unread_msg)
        return status

def see_follower(s):
	s.sendall(str(6))
	rc_msg=s.recv(1024)
	#print rc_msg
	show=''
	subscriber=[]
	od=1
	print'Your followee:'
	for a in rc_msg[2:]:
		if(a!='/'):
			show=show+a
		elif(a=='/'):
			print str(od)+':'+show
			subscriber.append(show)
			show=''
			od=od+1
	
def offline_msg(s,unread_msg):#msg_type 2
	num=0
	if(unread_msg==0):
		print'You have read all the messages.'
	else:
		while(num!=1 and num!=2 and num !=3):
			num=int(raw_input('offline message menu:\n1. see all messages\n2. see messages from someone\n3. go back to main menu\n'))
			msg=str(2)+str(num)
			if(num==1):#msg_type 21
				s.sendall(msg)
				rc_msg= s.recv(1024)
				print 'message:'	
				show=''
				od=1
				for a in rc_msg[3:]:
					if(a!='/' and a!='^' and a!='&' ):
						show=show+str(a)
					elif(a=='^'):
						show=(show)+' from '
					elif(a=='&'):
						show=show+' hashtag: '
					elif(a=='/'):
						print str(od)+':'+show
						show=''
						od=od+1
			elif(num==2):#msg_type 22
				print 'in 2 '+msg
				msg=msg+str(0)#msg_type 220
				#print msg
				s.sendall(msg)
				rc_msg=s.recv(1024)
				#print rc_msg
				show=''
				subscriber=[]
				od=1
				print'Your followee:'
				for a in rc_msg[4:]:
					if(a!='/'):
						show=show+a
					elif(a=='/'):
						print str(od)+':'+show
						subscriber.append(show)
						show=''
						od=od+1
				choice=input('choose someone above by their number:')
				while(int(choice)>od-1):
					choice=input('Please choose someone above by their number:')
				#print 'choice is '+str(choice)
				snd_msg=rc_msg[0:2]+str(1)+str(choice-1)#msg_type 221
				#print 'send message '+snd_msg
				s.sendall(snd_msg)
				#print subscriber[choice]
				rc_msg=s.recv(1024)
				#print 'rc_msg is '+rc_msg
				show=''
				od=1
				for a in rc_msg[4:]:
					if(a!='/' and a!='^' and a!='&' ):
						show=show+str(a)
					elif(a=='^'):
						show=(show)+' from '
					elif(a=='&'):
						show=show+' hashtag: '
					elif(a=='/'):
						print str(od)+':'+show
						show=''
						od=od+1
			elif(num==3):
				main_menu(status,s,unread_msg)
			else:
				print 'invalid input'

def edit_sub(s):#msg_type 3
	num=0
	snd_msg=str(3)
	while(num!=1 and num!=2 and num !=3):
		num=int(input('edit menu:\n1. delet a subscription\n2. add a subscription\n3. go back to main menu\n'))
		if(num==1):
			snd_msg=snd_msg+str(10)#msg_type 30
			print 'in 1 '+snd_msg
			s.sendall(snd_msg)
			snd_msg=''
			rc=''
			print rc
			rc= s.recv(1024)
			show=''
			subscriber=[]
			od=1
			print'Your followee:'
			for a in rc[4:]:
				if(a!='/'):
					show=show+a
				elif(a=='/'):
					print str(od)+':'+show
					subscriber.append(show)
					show=''
					od=od+1
			choice=input('choose one to delet(if u do not want to delete anyone, input 0):')
			while(int(choice)>od-1 and int( choice)!=0):
				choice=input('choose one to delet(if u do not want to delete anyone, input 0):')
			#print 'choice is '+str(choice)
			if(int(choice)!=0):
				snd_msg=rc[0:2]+str(1)+str(choice-1)#msg_type 311
				#print 'send message '+snd_msg
			s.sendall(snd_msg)
		elif(num==2):
			snd_msg=snd_msg+str(20)#320
			s.sendall(snd_msg)
			snd_msg=''
			rc=''
			rc= s.recv(1024)
			show=''
			subscriber=[]
			od=1
			print'User:'
			for a in rc[4:]:
				if(a!='/'):
					show=show+a
				elif(a=='/'):
					print str(od)+':'+show
					subscriber.append(show)
					show=''
					od=od+1
			choice=input('choose one to add(if u do not want to add anyone, input 0):')
			while(int(choice)>od-1 and int( choice)!=0):
				choice=input('choose one to add(if u do not want to add anyone, input 0):')
			#print 'choice is '+str(choice)
			if(int(choice)!=0):
				snd_msg=rc[0:2]+str(1)+str(choice-1)#msg_type 321
			print 'send message '+snd_msg
			s.sendall(snd_msg)
		elif(num==3):
			main_menu(status,s,unread_msg)
		else:
			print 'invalid input'
def post_msg(s):#msg_type 4
	msg=raw_input('Please input your message:')
	snd_msg=str(4)+msg
	s.sendall(snd_msg)
	
def hashtag_search(s):#msg_type 5
	key=raw_input('one hashtag you are interested in: ')
	key=re.sub('\n$','',key)
	snd_msg=str(5)+key
	#print snd_msg
	s.sendall(snd_msg)
	print 'search result is'
	rc_msg= s.recv(1024)
	#print rc_msg
	show=''
	od=1
	for a in rc_msg[2:]:
		if(a!='/' and a!='^' and a!='&' ):
			show=show+str(a)
		elif(a=='^'):
			show=(show)+' from '
		elif(a=='&'):
			show=show+' hashtag: '
		elif(a=='/'):
			print str(od)+':'+show
			show=''
			od=od+1

try:
	#create an AF_INET, STREAM socket (TCP)
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to creat socket. Error code: ' +str(msg[0]) + ', Error message :'+ msg[1]
	sys.exit();

print 'Socket Created'

host='localhost'
port=7878

try:

	remote_ip=socket.gethostbyname( host )

except socket.gaierror:
	#could not resove
	print 'hostname could not be resolved. Exiting'
	sys.exit()

print 'Ip address of '+ host+' is ' + remote_ip

#connect to remote server
s.connect((remote_ip, port))
print 'Socket Connected to ' + host + ' on ip '+remote_ip
log_in=1
while (log_in!=0):
	#log in begin
	msg_type=1#log in msg
	acc=raw_input('welcome!\naccount name:')
	acc=re.sub('\n$','',acc)
	code=getpass.getpass('password:')
	code=re.sub('\n$','',code)
	code[::-1]
	msg=str(msg_type)+acc+'!'+code
	try :
		#Set the whole string
		print'send succ'
		s.sendall(msg)
	except socket.error:
		#Send failed
		print 'Send failed'
		sys.exit()

	#Now receive data
	rc_msg= s.recv(1024)
	status=int(rc_msg[1:2])
	if( status==1 and int( rc_msg[0])==1):
		unread_msg=int(rc_msg[2:])
		print 'Log in success! You have '+ rc_msg[2:]+' messages unread.'
	# login finish
	while(status==1):
		status=main_menu(status,s,unread_msg)

	print 'If you want to log out, input 0'
	log_in=input();
	log_in=re.sub('\n$','',log_in)

s.close()
