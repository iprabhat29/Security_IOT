import cryptomath
import re
def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
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
    print pk,type(pk)
    key, n = pk
    
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)
    
def keygenfile():
    print "Generating your public/private keypairs now . . ."
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
    public, private = generate_keypair(p, q)
    outfile = open('publickey.txt','w')
    outfile.write("%s %s"%(public[0],public[1]))
    outfile.close()
    outfile=open('privatekey.txt','w')
    outfile.write("%s %s"%(private[0],private[1]))
    outfile.close()

def encfile(message):
    outfile= open('privatekey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    prituple = int(wordlist[0]),int(wordlist[1])
    encrypted_msg = encrypt(prituple, message)
    print "Your encrypted message is: "
    print ''.join(map(lambda x: str(x), encrypted_msg))
    outfile=open('encrypted','w')
    outfile.write(str(encrypted_msg))
    outfile.close()


def decfile():
    outfile= open('publickey.txt','r')
    word = outfile.read()
    outfile.close()
    wordlist = word.split()
    pubtuple = int(wordlist[0]),int(wordlist[1])
    print "Decrypting message with public key ", pubtuple ," . . ."
    print "Your message is:"
    outfile=open('encrypted','r')
    out = outfile.read()
    outfile.close()
    #print out
    newlist = []
    list1 = []
    out1 = re.sub('[^A-Za-z0-9\,]+',' ',out)
    #print out1
    #print decrypt(pubtuple, out2)
    newlist = out1.split(",")
    for word in newlist:
    	list1.append(long(word))
    print list1
    print decrypt(pubtuple,list1)
 
outfile = open('input.txt','r')
out = outfile.read()
enc = encfile(out)
outfile.close()
decfile()
