from RSA_crypto import *
import hashlib
import os
passkey = "Prabhat Bhatt"
key1 = hashlib.sha256(passkey).digest()
print " KEY1--->",passkey
keygenfile()
encfile(passkey,"1")
passkey1 = decfile("1")
print "Passkey after dec--->",passkey1
key2 = hashlib.sha256(passkey).digest()
if key1 == key2: 
	print "Key1--->",key1

pass1="ACK1 STATION"
encfile(pass1,"2")
hash1 = hashlib.sha256(pass1).digest()
dec = decfile("2")
hash2 = hashlib.sha256(dec).digest()


pass2 = "ACK2 STATION"
encfile(pass2,"3")
hash3 = hashlib.sha256(pass2).digest()
dec = decfile("3")
hash4 = hashlib.sha256(dec).digest()
if hash3 == hash4:
	print "Go ahead hash3 == hash4"

