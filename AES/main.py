from encryptor import *
import hashlib
import sys
infile = sys.argv[1]

password = "Prabhat"

key = hashlib.sha256(password).digest()

print key

encryptor(infile,'enc_file')
decryptor('enc_file','outfile')

