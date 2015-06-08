import socket
import sys
from thread import *
import re

HOST=''
PORT=7878

class User:
	def __init__(self,username,password):
		self.name=username
		self.pswd=password
		self.msg=[]
		self.conn=None
		self.follow_you=[]
		self.u_follow=[]
		self.unread=0
		self.online=0

user={}
user["jy"]=User("jy","1")
user["dead"]=User("dead","2")
#user["jy"].u_follow.append(user["dead"])
user["no"]=User("no","3")
user["jy"].u_follow.append(user["no"])
user["dead"].u_follow.append(user["jy"])

class Message:
	def __init__(self,content,author,hashtag):
		self.content=content
		self.author=author
		self.hashtag=hashtag
		self.read=0

msgs=[]
hashtag1="a b c"
hashtag1.split(' ')
msg1=Message("com on",user["jy"],hashtag1)
msgs.append(msg1)
hashtag2="a b c"
hashtag2.split(' ')
msg2=Message("2nd",user["dead"],hashtag2)
msgs.append(msg2)

user["dead"].unread=user["dead"].unread+1
user["dead"].msg.append(msg1)

user["jy"].msg.append(msg2)
user["jy"].unread=user["jy"].unread+1

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((HOST,PORT))
except socket.error , msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + 'Message' + msg[1]
	sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socker now listening'

connectList=[]
#Function for handling connections. This will be used to creat threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n')#send only takes string

	#infinite loop so that function do not terminate and thread do not end.
	while True:
		
		#Receriving frong client
		data =conn.recv(1024)
		if data[0:12]=='Send to all:':
			for member in connectList:
				reply=data[12:]
				member.sendall(reply)
		if data[0:12]!='Send to all:':
			reply = 'OK...'+data
			conn.sendall(reply)
		if not data:
			break

	#came out of loop
	conn.close
	connectList.remove(conn)

def twitter(conn):
	print 'in twitter'
	rc=conn.recv(1024)
	msg_type=rc[0:1]
	msg=rc[1:]
	#print'msg_type: '+msg_type+' msg: '+msg
	username=''
	password=''
	if(int(msg_type)==1):
		print'msg_type1 succ: '+msg
		inname=1
		pswd=''
		for x in msg[0:]:
			#print'x: '+x+' inname: '+str(inname)
			if( x!='!' and inname==1):
				username=username+x
			#	print 'username : '+username
			if(x=='!'):
				inname=0
			if(x!='!' and inname==0):
				password=password+x
			#print'in for username: '+username+' inname: '+str(inname)
		if username in user.keys():
			pswd=user[username].pswd
			if(pswd==password):
				status=1
				user[username].conn=conn
				rply_msg=msg_type+str(status)+str(user[username].unread)
				user[username].online=1
			else:
				status=0
				rply_msg=msg_type+str(status)
		else:
			status=0
			rply_msg=msg_type+str(status)
		#print'msg: '+str(msg)
		conn.sendall(rply_msg)	
	while(status==1):		
		rc=conn.recv(1024)
		print 'always here rc msg is '+rc
		msg_type=rc[0]
		snd_msg=''
		print 'receive message: '+rc
		if(int(rc[0])==2):#msg_type 2
			if(int(rc[1])==1):#msg type 21
				snd_msg=str(21)
	 			for a in user[username].msg:
					snd_msg=snd_msg+'/'+str(a.content)+'^'+str(a.author.name)+'&'+str(a.hashtag)
				snd_msg=snd_msg+str('/')
				print snd_msg
				conn.sendall(snd_msg)
			elif(int(rc[1])==2):#msg_type 22
				snd_msg=str(22)
				if(int(rc[2])==0):#msg_type 220
					print '220'
					snd_msg=snd_msg+str(0)
					for a in user[username].u_follow:
						snd_msg=snd_msg+str('/')+str(a.name)
					snd_msg=snd_msg+str('/')
					print snd_msg
					conn.sendall(snd_msg)
				elif(int(rc[2])==1):#msg_type 221
					print '221'
					snd_msg=snd_msg+str(1)
					choice=int(rc[3:])
					od=0
					interest_name=''
					for a in user[username].u_follow:
						if(od==choice):
							interest_name=str(a.name)
							print 'find '+ interest_name
						od=od+1
					for a in user[username].msg:
						if (a.author.name==interest_name):
							snd_msg=snd_msg+'/'+str(a.content)+'^'+str(a.author.name)+'&'+str(a.hashtag)
					snd_msg=snd_msg+str('/')
					print snd_msg
					conn.sendall(snd_msg)
		elif(int(rc[0])==3):
			snd_msg=str(3)
			if(int(rc[1])==1):#delete
				if(int(rc[2])==0):#send followee
					print '310'
					snd_msg=snd_msg+str(10)#310
					for b in user[username].u_follow:
						print b
						snd_msg=snd_msg+str('/')+str(b.name)
					snd_msg=snd_msg+str('/')
					print 'send: '+snd_msg+' '+str(len(snd_msg))
					conn.sendall(snd_msg)
				elif(int(rc[2])==1):#311 choice to delete
					print rc
					choice=int(rc[3:])
					user[username].u_follow.pop(choice)
					print user[username].u_follow						
			elif(int(rc[1])==2):
				if(int(rc[2])==0):
					print '320'
					snd_msg=snd_msg+str(20)#320
					for b in user.keys():
						snd_msg=snd_msg+'/'+b
					snd_msg=snd_msg+'/'
					print snd_msg
					conn.sendall(snd_msg)
				elif(int(rc[2])==1):#321 choice to delete
					print rc
					choice=int(rc[3:])
					print 'choice is '+str(choice)
					od=0
					for a in user.keys():
						print a+' '+ username
						if(od==choice and not a in user[username].u_follow and a!=username):
							user[username].u_follow.append(user[a])
							print'add it' 
						od=od+1
					print user[username].u_follow						
		elif(int(rc[0])==4):#4
			msg=rc[1:]
			msg=re.sub('\n','',msg)
			author=username
			content=''
			od=0
			for a in msg:
				od=od+1
				if(a=='#'):
					break
				content=content+a
			hashtagtmp=msg[od:]
			hashtagtmp.split('#')
			msgtmp=Message(content,user[author],hashtagtmp)
			msgs.append(msgtmp)
			print msgs
			for a in user.keys():
				#print 'a '+user[a].name
				for b in user[a].u_follow :
					#print 'b '+b.name
					if (b.name==username):
						#print '= ,username:'+username#+' b.conn'+b.conn
						if(user[a].conn==None):
						#	print 'stored'
							user[a].msg.append(msgtmp)
							user[a].unread=user[a].unread+1
						else:
							user[a].msg.append(msgtmp)
							user[a].unread=user[a].unread+1
							#snd_msg=str(4)
							#snd_msg=snd_msg+'/'+content+'^'+author+'&'+hashtagtmp+str('/')
							#user[a].conn.sendall(snd_msg)
		elif(int(rc[0])==0):
			status=0
		elif(int(rc[0])==5):
			#print '5'
			hashtag=rc[1:]
			#print 'search for: '+hashtag
			snd_msg=str(5)
			for a in msgs:
				for b in a.hashtag:
			#		print 'message hashtag is '+b
					if (b==hashtag):
			#			print '='
						snd_msg=snd_msg+'/'+str(a.content)+'^'+str(a.author.name)+'&'+str(a.hashtag)
			snd_msg=snd_msg+'/'
			conn.sendall(snd_msg)
	print 'clear'
	user[username].online=0
	user[username].conn=None
	user[username].unread=0
	user[username].msg=[]
#now keep talking with the client
while 1:
	#wait to accpt a connection - blocking call
	conn, addr= s.accept()
	connectList.append(conn)

	#display client information
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to sun, second is the tuple of arguments to the function.
	start_new_thread(twitter,(conn,))

s.close()
