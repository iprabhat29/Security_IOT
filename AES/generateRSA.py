from Crypto.PublicKey import RSA 
new_key = RSA.generate(1024, e=65537) 
public_key = new_key.publickey().exportKey("PEM") 

file1 = open('RSA_ID_pub','wb')
file1.write(public_key)
file1.close()


private_key = new_key.exportKey("PEM")
file2 = open('RSA_ID_pri','wb')
file2.write(private_key)
file2.close()
