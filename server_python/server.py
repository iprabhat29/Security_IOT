import logging
import os,random,sys,hashlib,struct,thread,socket

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

SUBSTATION_FILEPATH = "/home/user/iprabhat/TW_project/substation"

LOCAL_PRIVATE_KEY = "/home/user/iprabhat/TW_Project/KEY/PrivateRSA"

LOCAL_PUBLIC_KEY = "/home/user/iprabhat/TW_Project/KEY/PublicRSA"

HOME = os.path.expanduser("~")

Server_machine_ip = "localhost"

Server_machine_port = 8080

#Authenticity with MAC , stationid, PWD


#send validation result from validation function
# if a function is validated it will send 1 if not will send 0

def send_valid_result(result):
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Open TCP connection
	sock1.connect((CLIENT_HOST,TCP_CON_PORT))			#connect to the client
	sock1.send(result)						#send the result of the validation
	sock1.close()

def server_validation(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)		#create TCP socket
	sock.setsockopt(socket.SOL_SOCKET,SO_REUSEADDR,1)	#set option for socket for addres resue
	sock.bind(("0.0.0.0",port))	#binding the server to all interface available
	sock.listen(5)			#listing to accept connection
	(client,(ip,cport)) = sock.accept()	#accept a socket connection
	data = client.recv(1024)	#start receiving 1024 byte at a time
	if data == 1:
		print "INTEGRITY VALIDATION PASSED!!!"
	else:
		print "INTEGRITY VALIDATION FAILED!!!"
	os.exit(0)



def validate_client_integrity(sourcehash,destfilepath):	#validatingfile integrity
	desthash = hashlib.md5(open(destfilepath,"rb").read()).hexdigest() #calculating hash of file sent
	if(sourcehash == desthash):	#if hashes are equal send 1 and return TRUE
		send_valid_result("1")
		return True
	else:
		os.system("rm"+destfilepath)	#if hashes are not equal send 0 and False
		send_valid_result("0")
		return False

class MyHandler(FTPHandler):
	def file_recv(self,filepath):
		decrypt(filepath)
		os.system("rm"+filepath)
	

def encryption(filepath):
	print "STARTING ENCRYPTION..."
	AES_key = os.urandom(32)		#using 32 bit key by randomly generating it
	out_file_name = filepath + ".enc"
	FILE_HASH = hashlib.md5(open(filepath).read()).hexdigest()
	
	#public key encryption of the symmetric key

	pubkey = open(LOCAL_PUBLIC_KEY,"r").read()
	RSA_KEY = RSA>importkey(pubkey)
	RSA_KEY = PKCS1.OAEP.new(RSA_KEY)
	ENCY_KEY = RSA_KEY.encrypt(AES_key)
	outfile = open(out_file_name,"w+")
	
	outfile.write(FILE_HASH)
	outfile.write(ENCY_KEY)
	IV = ''.join(chr(random.randint(0,0xFF)) for i in range(16))
	enc = AES.new(AES_key , AES.MODE_CBC,iv)   # creating new encryptor object
	filesize = os.path.getsize(filepath)		#size of the orignal file being send
	blocksize = 64*1024		#size of block
	
	with open(filepath,'rb') as infile:
		outfile.write(struct.pack('<Q',filesize)) #intepreting data of the file to binary
		outfile.write(iv)  #writing iv to the file which will be used to generate the first block of data
		while True:
			chunkfile = infile.read(blocksize)
			if len(chunkfile)==0:
				break
			elif len(chunkfile) % 16 !=0:
				chunkfile+=' ' *(16-len(chunkfile)%16)  #pad the file if not in chunk of 16bytes
			outfile.write(encypt.encryption(chunkfile))

	outfile.close()
	print "Encryption done..."
	return out_file_name

def server_start():
	auth = DummyAuthorizer()	#FTP authorizer
	authorizer.add_anonymous(HOME + "/anonymous", perm='elradfmwM')
	handler = MyHandler
	handler.authorizer = authorizer
	handler.banner = "Server Ready..."
	hostname = ""
	address = (hostname,8080)
	server = FTPServer(address,handler)
	server.max_cons = 10
	server.serve_forever()

def main():
	server_start()

if __name__=="__main__":
	main()	
