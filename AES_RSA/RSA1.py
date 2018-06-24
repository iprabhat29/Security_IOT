import cryptomath
import random
import math

def keygen(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = cryptomath.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = cryptomath.gcd(e, phi)
    d = cryptomath.multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = int(pk[0]),int(pk[1])
    print type(key),type(n)
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = int(pk[0]),int(pk[1])
    plain = [chr((char ** key) % n) for char in ciphertext]
    print plain
    return ''.join(plain)


def keyfilegen():

    primes = []
    num = 3
    while True:
    	while num <= 999:
    		for i in range(3,num):
    			if num % i == 0:
    				break
    		else:
    			primes.append(num)	
    		num = num + 1	
        p = random.choice(primes)
        q = random.choice(primes)
    	if p != q:
    		break
    print p,q
    public, private = keygen(p, q)
    print public,private
    outfile = open("publickey.txt","w")
    outfile.write(" ".join([str(public[0]),str(public[1])]))   
    outfile.close()
    outfile = open("privatekey.txt","w")
    outfile.write(" ".join([str(private[0]),str(private[1])]))
    outfile.close()

def encmain(message):
    public = []
    private = []
    outfile = open("publickey.txt","r")
    public = outfile.read()
    outfile.close()
    print "PUBLIC FILE" , public 
    outfile1 = open("privatekey.txt","r")
    private = outfile1.read()
    outfile.close()
    print "PRIVATE FILE" , private
    encrypted_msg = encrypt(private, message)
    print "Your encrypted message is: "
    print ''.join(map(lambda x: str(x), encrypted_msg))
    print "Decrypting message with public key ", public ," . . ."
    print "Your message is:"
    print decrypt(public, encrypted_msg)
    
if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    keyfilegen()
    encmain("hello")

