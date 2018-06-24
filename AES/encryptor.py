
import os, random, sys, hashlib, struct, thread, socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

Priv_key = "/Users/iprabhat/TW_Project_python/AES/RSA_ID_pri"
Pub_key = "/Users/iprabhat/TW_Project_python/AES/RSA_ID_pub"



def valInt(orighash,file_out):
	desthash = hashlib.md5(open(file_out,"rb").read()).hexdigest()
	if(orighash == desthash):
		return True
	else:
		os.system("rm"+file_out)
		return False


def encryptor(file_in,file_out=None,chunk_size = 64*1024):
	#file_in --> input file
	#file_out-->Output file if none '<file_in>.enc' will be used
	#Chunk_size-->Divisible by 16 (16 bytes)

	if not file_out:
		file_out = file_in + '.enc'


	IV = os.urandom(16)
	
	publickey = Pub_key
	AES_key  = os.urandom(32)
	filehash = hashlib.md5(open(file_in).read()).hexdigest()
	pubkey = open(publickey,"rb")
	rsakey = RSA.importKey(pubkey.read())
	rsakey = PKCS1_OAEP.new(rsakey)
	enckey = rsakey.encrypt(AES_key)
	fileout = open(file_out,"w+")
	fileout.write(filehash)
	fileout.write(enckey)
	
	
	
	ency = AES.new(AES_key,AES.MODE_CBC,IV)

	size_file_in = os.path.getsize(file_in)

	with open(file_in,'rb') as filein:
		fileout.write(struct.pack('<Q',size_file_in))
		fileout.write(IV)

		while True:
			chunk = filein.read(chunk_size)
			if len(chunk) == 0:
				break
			elif len(chunk)% 16 != 0:
				chunk +=' ' * (16 - len(chunk)%16)
			fileout.write(ency.encrypt(chunk))


	fileout.close()

def decryptor(file_in, file_out=None, chunk_size=64*1024):
#Decrypting file using AES key given hardcoded.
	if not file_out:
		file_out = os.path.splitext(file_in)[0]

	infile = open(file_in,"r")
	hash = infile.read(32)
	encAESkey = infile.read(512)
	
	priv_key = Priv_key
	privkey = open(priv_key,"r").read()
	rsakey = RSA.importKey(privkey)
	rsakey = PKCS1_OAEP.new(rsakey)
	aes_key = rsakey.decrypt(encAESkey)

	size = struct.unpack('Q',infile.read(struct.calcsize('Q')))[0]
	IV = infile.read(16)

	decry = AES.new(aes_key,AES.MODE_CBC,IV)

        with open(file_out, 'wb') as fileout:
            	while True:
                	chunk = infile.read(chunk_size)
                	if len(chunk) == 0:
                    		break
                	fileout.write(decry.decrypt(chunk))
		fileout.truncate(size)

	print "File decrypted sucessfully!!!"

	print "Validating Integrity\n"

	if(valInt(hash,file_out)):
		print "Integrity passed"
	else:
		print "Integrity Failed"

