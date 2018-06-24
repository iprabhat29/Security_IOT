#import cryptomath
import re
import random
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi


def generate_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    #print pk,type(pk)
    key, n = pk
    
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
    
def keygenfile():
    #print "Generating your public/private keypairs now . . ."
    primes = []
    num = 3
    while True:
    	while num <= 99:
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
    #print p,q
    public, private = generate_keypair(p, q)
    outfile = open('publickey.txt','w')
    outfile.write("%s %s"%(public[0],public[1]))
    outfile.close()
    outfile=open('privatekey.txt','w')
    outfile.write("%s %s"%(private[0],private[1]))
    outfile.close()

def enc2(message):
	outfile = open('privatekey.txt','r')
	word = outfile.read()
	outfile.close()
	wordlist = word.split()
	prituple = int(wordlist[0]),int(wordlist[1])
	return encrypt(prituple,message)

def dec2(message):
	outfile = open('publickey.txt','r')
	word = outfile.read()
	outfile.close()
	wordlist = word.split()
	pubtuple = int(wordlist[0]),int(wordlist[1])
	return decrypt(pubtuple,message) 

	
def encfile(message,filenumber):
    outfile= open('privatekey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    prituple = int(wordlist[0]),int(wordlist[1])
    encrypted_msg = encrypt(prituple, message)
    #print "Your encrypted message is: "
    #print ''.join(map(lambda x: str(x), encrypted_msg))
    fileout = "encrypted"+filenumber
    outfile=open(fileout,'w')
    outfile.write(str(encrypted_msg))
    outfile.close()
    


def decfile(filenumber):
    outfile= open('publickey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    pubtuple = int(wordlist[0]),int(wordlist[1])
    #print "Decrypting message with public key ", pubtuple ," . . ."
    #print "Your message is:"
    fileout = "encrypted"+filenumber
    outfile=open(fileout,'r')
    out = outfile.read()
    outfile.close()
    #print "ENCRYPTED--->",out
    newlist = []
    list1 = []
    out1 = re.sub('[^A-Za-z0-9\,]+',' ',out)
    #print out1
    #print decrypt(pubtuple, out2)
    newlist = out1.split(",")
    for word in newlist:
    	list1.append(long(word))
    #print list1
    msg = decrypt(pubtuple,list1)
    return msg

def encfile2(message):
    outfile= open('privatekey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    prituple = int(wordlist[0]),int(wordlist[1])
    encrypted_msg = encrypt(prituple, message)
    #print "Your encrypted message is: "
    #print ''.join(map(lambda x: str(x), encrypted_msg))
    outfile=open('encrypted2','w')
    outfile.write(str(encrypted_msg))
    outfile.close()
    


def decfile2():
    outfile= open('publickey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    pubtuple = int(wordlist[0]),int(wordlist[1])
    #print "Decrypting message with public key ", pubtuple ," . . ."
    #print "Your message is:"
    outfile=open('encrypted2','r')
    out = outfile.read()
    outfile.close()
    #print "ENCRYPTED--->",out
    newlist = []
    list1 = []
    out1 = re.sub('[^A-Za-z0-9\,]+',' ',out)
    #print out1
    #print decrypt(pubtuple, out2)
    newlist = out1.split(",")
    for word in newlist:
    	list1.append(long(word))
    #print list1
    msg = decrypt(pubtuple,list1)
    return msg


def encfile3(message):
    outfile= open('privatekey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    prituple = int(wordlist[0]),int(wordlist[1])
    encrypted_msg = encrypt(prituple, message)
    #print "Your encrypted message is: "
    #print ''.join(map(lambda x: str(x), encrypted_msg))
    outfile=open('encrypted3','w')
    outfile.write(str(encrypted_msg))
    outfile.close()
    


def decfile3():
    outfile= open('publickey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    pubtuple = int(wordlist[0]),int(wordlist[1])
    #print "Decrypting message with public key ", pubtuple ," . . ."
    #print "Your message is:"
    outfile=open('encrypted3','r')
    out = outfile.read()
    outfile.close()
    #print "ENCRYPTED--->",out
    newlist = []
    list1 = []
    out1 = re.sub('[^A-Za-z0-9\,]+',' ',out)
    #print out1
    #print decrypt(pubtuple, out2)
    newlist = out1.split(",")
    for word in newlist:
    	list1.append(long(word))
    #print list1
    msg = decrypt(pubtuple,list1)
    return msg
