






def validateIntegrity(orighash, destfilepath):			# Validate the integrity of the received file
	desthash = hashlib.md5(open(destfilepath, "rb").read()).hexdigest()		# calculate the received and decrypted file's MD5 checksum
	if(orighash==desthash):
		send_validation_result("1")
		return True 						# If the original hash matches the decrypted file's hash, return true		
	else:
		os.system("rm "+destfilepath)		# If two hashed do not match, file is either corrupted or modified in the middle. So delete the file..
		send_validation_result("0")
		return False						# ..and return false

def decrypt(filepath):						# function to decrypt files
	print "[!] Starting decryption...."
	dec_filename = ANONYMOUS_FILEPATH + os.path.basename(filepath).strip(".enc")
	inFile = open(filepath,"r")				# open the file to be decrypted as read-only
	chunksize=64*1024						# set the chunk size which is used as the block for block decryption
	hash = inFile.read(32)					# read the first 32 bytes from the file which contains the original file's hash		
	encAESKey = inFile.read(512)			# read second 512 bytes which is the RSA enrypted AES symmetric key
	
	#####decrypt AES symmetric key using RSA decryption with private key####
	private_key_loc = PRIV_KEY_LOC			
	privkey = open(private_key_loc, "r").read()			# open the SSH private key used for decryption
	rsakey = RSA.importKey(privkey)
	rsakey = PKCS1_OAEP.new(rsakey)						# use OAEP to create cipher for decryption
	aes_key = rsakey.decrypt(encAESKey) 				# decrypt the AES symmetric key using RSA decryption
	########################################################################

	origsize = struct.unpack('<Q', inFile.read(struct.calcsize('Q')))[0]	# calculate the original file size
	iv = inFile.read(16)								# extract next 16 bytes as the 16 bytes initialization vector 
	decryptor = AES.new(aes_key, AES.MODE_CBC, iv)		# create new AES Decryptor object

	with open(dec_filename, 'wb') as outfile:
		while True:
			chunk = inFile.read(chunksize)
			if len(chunk) == 0:
				break
			outfile.write(decryptor.decrypt(chunk))		# decrypt the file chunk by chunk using the created decryptor 
		
		outfile.truncate(origsize)						# truncate the decrypted file to the original size 
	
	print "[+] File was decrypted and saved at \""+dec_filename+"\""
	
	print "[!] Validating integrity..."
	if (validateIntegrity(hash, dec_filename)):			# call the integrity validator, pass the extracted original file's hash and the decrypted file's location to the function
		print "[+] Integrity validation Passed!"
	else:
		print "[-] Integrity validation Failed!"
	
	return dec_filename
	
def encrypt(filepath):
	print "[!] Starting Encryption...."
	aes_key = os.urandom(32)			# generate a 32 bit secret key using the random number generator
	out_filename = filepath + ".enc"
	filehash = hashlib.md5(open(filepath).read()).hexdigest()		# calculate the MD5 hash of the file to be sent
	
	public_key_loc = PUB_KEY_LOC
	#public key encryption of the symmetric key
	pubkey = open(public_key_loc, "r").read()			# open the SSH public key of the destination server
	rsakey = RSA.importKey(pubkey)						# import the public key
	rsakey = PKCS1_OAEP.new(rsakey)						# create the cipher using OAEP with RSA
	encKey = rsakey.encrypt(aes_key)					# encrypt the generated 21 bit AES key to be shared with the server
	outFile = open(out_filename,"w+")					# Open a new file which will be our encrypted file
	
	outFile.write(filehash)							# write the calculated MD5 hash of the original file at the begining of the file
	
	outFile.write(encKey)							# then, write the encrypted AES key, to the file
	
	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))	# generate a 16 byte IV - Initialization vector which is used by AES algorithm with CBC to encrypt the first block of the file
	encryptor = AES.new(aes_key, AES.MODE_CBC, iv)	# create a new encryptor object
	filesize = os.path.getsize(filepath)			# calculate the size of the original file which we are going to encrypt
	chunksize=64*1024								# initialize chunk size for block encryption
	
	with open(filepath, 'rb') as infile:
		outFile.write(struct.pack('<Q', filesize)) 	# interpret the data string of the file as a packed binary data. This is needed at the destination to truncate the file to its original size.
		outFile.write(iv)							# write the generated IV to the file. IV is needed by the destination to decrypt only the first block of encrypted data
		
		while True:
			chunk = infile.read(chunksize)			# read a chunk of data from the file
			if len(chunk) == 0:						
				break								# if the chunk is empty, obviously file has been completed reading. So break the reading operation
			elif len(chunk) % 16 != 0:
				chunk += ' ' * (16 - len(chunk) % 16)	# if the chunk's size is not a multiple of 16 bytes, it needs to be padded so that it can be block encrypted. So add spaces as paddinig
			outFile.write(encryptor.encrypt(chunk))		# encrypt the chunk and write the encrypted chunk to the file
	
	outFile.close()
	print "[+] Encryption successful!"
	return out_filename	
