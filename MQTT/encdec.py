
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import base64
import StringIO

# passphrase, random string => private key, public key pair
# encrypt with public key
# decrypt with pem, passphrase

def gen_key_pair(passphrase):
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    return key.exportKey(passphrase=passphrase), key.publickey().exportKey()

def rsa_encrypt(message, pub):
    keystream = StringIO.StringIO(pub)
    pubkey = RSA.importKey(keystream.read())
    h = SHA.new(message)
    cipher = PKCS1_v1_5.new(pubkey)
    return base64.encodestring(cipher.encrypt(message+h.digest()))

def rsa_decrypt(ciphertext, pem, passphrase):
    ciphertext = base64.decodestring(ciphertext)
    keystream = StringIO.StringIO(pem)
    pemkey = RSA.importKey(keystream.read(), passphrase=passphrase)
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(pemkey)
    message = cipher.decrypt(ciphertext, sentinel)
    digest = SHA.new(message[:-dsize]).digest()
    if digest == message[-dsize:]:
        return message[:-dsize]
    else:
        raise ValueError('Cannot decrypt message')

def encfile(pub,message,outfilename):
	file = open(outfilename,"a")
	encdata = rsa_encrypt(message,pub) 
	file.write(encdata)
	file.close()

# pem, pub = gen_key_pair(passphrase)

def decfile(infilename,outfilename,pem,passphrase):
	file1 = open(infilename,"rb")
	file2 = open(outfilename,"a")
	for line in file1:
		decdata = rsa_decrypt(line, pem, passphrase)
		file2.write(decdata)
	file2.close()
	file1.close()
    	

#print 'Decrypted Message:\n', decdata
