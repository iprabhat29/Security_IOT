import os,random,struct
import Crypto.Random
from Crypto.Cipher import AES
import Crypto

def encryptor(key,file_in,file_out=None,chunk_size = 64*1024):
	#file_in --> input file
	#file_out-->Output file if none '<file_in>.enc' will be used
	#Chunk_size-->Divisible by 16 (16 bytes)

	if not file_out:
		file_out = file_in + '.enc'


	IV = os.urandom(16)
	ency = AES.new(key,AES.MODE_CBC,IV)
	size_file_in = os.path.getsize(file_in)

	with open(file_in,'rb') as filein:
		with open(file_out,'wb') as fileout:
			fileout.write(struct.pack('<Q',size_file_in))
			fileout.write(IV)

			while True:
				chunk = filein.read(chunk_size)
				if len(chunk) == 0:
					break
				elif len(chunk)% 16 != 0:
					chunk +=' ' * (16 - len(chunk)%16)
				fileout.write(ency.encrypt(chunk))


def pad_data(data):
    if len(data) % 16 == 0:
        return data
    databytes = bytearray(data)
    padding_required = 15 - (len(databytes) % 16)
    databytes.extend(b'\x80')
    databytes.extend(b'\x00' * padding_required)
    return bytes(databytes)

def unpad_data(data):
    if not data:
        return data

    data = data.rstrip(b'\x00')
    if data[-1] == 128: # b'\x80'[0]:
        return data[:-1]
    else:
        return data


def generate_aes_key():
    rnd = Crypto.Random.OSRNG.posix.new().read(AES.block_size)
    return rnd

def encrypt(key, iv, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = pad_data(data)
    return aes.encrypt(data)

def decrypt(key, iv, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = aes.decrypt(data)
    return unpad_data(data)

def enc_crypto (msg):
    print("Same IVs same key:")
    key = generate_aes_key()
    iv = generate_aes_key()
    #msg = b"This is some super secret message.  Please don't tell anyone about it or I'll have to shoot you."
    code = encrypt(key, iv, msg)
    return code,key,iv

def dec_crypto (key, msg, iv):
    decoded = decrypt(key, iv, msg)
    return decoded


def decryptor(key, file_in, file_out=None, chunk_size=24*1024):

#Decrypting file using AES key given hardcoded.

    if not file_out:
        file_out = os.path.splitext(file_in)[0]

    with open(file_in, 'rb') as filein:
        size = struct.unpack('<Q', filein.read(struct.calcsize('Q')))[0]
        iv = filein.read(16)
        decry = AES.new(key, AES.MODE_CBC, iv)

        with open(file_out, 'wb') as fileout:
            while True:
                chunk = filein.read(chunk_size)
                if len(chunk) == 0:
                    break
                fileout.write(decry.decrypt(chunk))

            fileout.truncate(size)
