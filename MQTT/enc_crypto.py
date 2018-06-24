#c!/usr/bin/env python

from Crypto.Cipher import AES
import base64
import os

# the block size for the cipher object; must be 16 per FIPS-197
BLOCK_SIZE = 16

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# generate a random secret key
#secret = os.urandom(BLOCK_SIZE)
#cipher = AES.new(secret)
cipher = os.urandom(16)
# create a cipher object using the random secret
def enc(msg):
	#cipher = AES.new(secret)
	# encode a string
	encoded = EncodeAES(cipher, msg)
	print "Encoding with sercret key ",secret
	print 'Encrypted string:', encoded
	#print "Encoding cipher ",cipher
	
	return encoded
def dec(encoded):
# decode the encoded string
	#cipher = AES.new(secret)
	print "Decoding String ",encoded
	print "Decoding with Secret Key ",secret
	#print "Decoding with cipher ",cipher
	decoded = DecodeAES(cipher,encoded)
	return decoded

	
