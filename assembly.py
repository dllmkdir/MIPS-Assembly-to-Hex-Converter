exMIPS1='exMIPS1.txt'
exMIPS2='exMIPS2.txt'
exMIPS3='exMIPS3.txt'

stresult="signal ROM : memoria_rom := (x\"00000000\", x\"00000000\", x\"00000000\", x\"00000000\", "
c=0
binstr=""
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
with open(exMIPS3) as assemblyCode:
	text= assemblyCode.readlines()
	for line in text:
		tokenizer = RegexpTokenizer(r'\-*\w+')
		token=tokenizer.tokenize(line)
		if(token[0]=="ADDI"):
			binstr="001000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			if(int(token[3])>=0):
				binstr+='{0:016b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			else:
				binstr+='{0:016b}'.format(int(token[3]) & 0b1111111111111111)

		elif(token[0]=="ADD"):
			binstr="000000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+="00000100000"
		elif(token[0]=="AND"):
			binstr="000000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+="00000100100"
		elif(token[0]=="OR"):
			binstr="000000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+="00000100101"
		elif(token[0]=="SUB"):
			binstr="000000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+="00000100010"
		elif(token[0]=="SLT"):
			binstr="000000" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+="00000101010"
		elif(token[0]=="SLL"):
			binstr="000000" #opcode
			binstr="00000" #ask for the s parameter
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+="000000"
		elif(token[0]=="SRL"):
			binstr="000000" #opcode
			binstr="00000" #ask for the s parameter
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+="000010"
		elif(token[0]=="SW"):
			binstr="101011" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:016b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))#ASK IF iiii is equal to offset
			
		elif(token[0]=="LW"):
			binstr="100011" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:016b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))#ASK IF iiii is equal to offset
			
		elif(token[0]=="BEQ"):
			binstr="000100" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:016b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))#ASK IF iiii is equal to offset
			
		elif(token[0]=="NOP"):#no operation
			binstr="00000000000000000000000000000000"
		elif(token[0]=="BNE"):
			binstr="000101" #opcode
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			binstr+='{0:05b}'.format(int(''.join(list(filter(str.isdigit, token[2])))))
			binstr+='{0:016b}'.format(int(''.join(list(filter(str.isdigit, token[3])))))#ASK IF iiii is equal to offset	
		elif(token[0]=="J"):
			binstr="000010" #opcode
			if(int(token[1])>=0):#could be negative
				binstr+='{0:026b}'.format(int(''.join(list(filter(str.isdigit, token[1])))))
			else:
				binstr+='{0:026b}'.format(int(token[1]) & 0b11111111111111111111111111)

		else:
			binstr="00000000000000000000000000000000"#wrong command
		stresult+="x\""+str('0x%08x' % int(binstr, 2)).upper()[2:]+"\""
		stresult +=", x\"00000000\", x\"00000000\", x\"00000000\", "
		c+=1
		#for tokeni in token:
			#print(tokeni)
assemblyCode.close()
n=255-c
for x in range(n):
	stresult +="x\"00000000\", x\"00000000\", x\"00000000\", x\"00000000\", "
stresult +="x\"00000000\", x\"00000000\", x\"00000000\", x\"00000000\");"
print(stresult)	

