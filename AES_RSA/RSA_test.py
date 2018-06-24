from RSA_crypto import *
import re
keygenfile()
infile = open("input.txt","r")
line = infile.read()
enc = encfile(line)
#print "ENC--->",enc[0]
#print "ENC STR 0",str(enc[0])
#print "ENC--->",enc
#decfile(enc)
#print type(enc)
#infile.close()

infile = open("encinput","w")
infile.write(str(enc))
infile.close()

#print "FILE WRITTEN\n"

outfile = open("encinput","r")
out = outfile.read()
#print "OUTFILE READING--->",out,type(out)
outfile.close()

out1 = re.sub('[^A-Za-z0-9]+',' ',out)
out2 =  out1.split()
newlist = []
for l in out2:
#	print l
	newlist.append(long(l))
#print "NEW list",newlist
#print out2[0]
content = decfile(newlist)

print content,type(content)
