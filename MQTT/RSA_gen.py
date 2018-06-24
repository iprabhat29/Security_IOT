import random 
import sys
import os
import rsamath
import prime


def keygen():
	p = prime.generateLargePrime(32)
	q = prime.generateLargePrime(32)
	n = p*q
#calculating e relative prime to p-1 and q-1

	while True:
		e = random.randrange(2 **(1023),2 **(1024))
		if rsamath.gcd(e,(p-1)*(q-1)) == 1:
			break

	#calculate d mod inverse of e

	d = rsamath.findModInverse(e,(p-1)*(q-1))

	public_key = (n,e)
	private_key = (n,d)

	print "PUBLIC KEY\n",public_key
	print "Private Key\n",private_key
	return (public_key,private_key)

def genkeypairfile():
	pubkey,privkey = keygen()
	print "Writing public key to a file"
	outfile = open("publicKey.txt","wb")
	outfile.write('%s,%s,%s'%(1024,pubkey[0],pubkey[1]))
	outfile.close()

	print "Writing Private key file"
	outfile = open("privatekey.txt","wb")
	outfile.write('%s,%s,%s'%(1024,privkey[0],privkey[1]))
	outfile.close()


keygen()
genkeypairfile()

