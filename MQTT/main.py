from encdec import *

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import base64
import StringIO
passphrase = "Prabhat Bhatt"
pem,pub = gen_key_pair(passphrase)
message = "dadadadadwiyuyuyuaghdvahdfygwhenwb"
encfile(pub,message,'outfile')
decfile('outfile','decfile',pem,passphrase)
