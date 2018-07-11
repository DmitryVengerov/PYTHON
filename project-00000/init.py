# encryotion algorithms
# This method is made only for the Latin alphabet

def encrypt_caesar(plaintext):
	enCode = plaintext
	deCode = ''
	lenS = len(enCode)

	if enCode.isalpha():
		for i in range(0, lenS):
			#print(enCode[i], ord(enCode[i]), chr(ord(enCode[i])+3), ord(enCode[i])+3)
			if ord(enCode[i]) > 119 or 87 < ord(enCode[i]) < 97:
				deCode += chr(ord(enCode[i])-23)
			else:
				deCode += chr(ord(enCode[i])+3)

		print('Encrypted string: ',deCode);
	else:
		print('You must enter only letters');

def decrypt_caesar(plaintext):
	deCode = plaintext
	enCode = ''
	lenS = len(deCode)

	if deCode.isalpha():
		for i in range(0, lenS):
			#print(deCode[i], ord(deCode[i]), chr(ord(deCode[i])-3), ord(deCode[i])-3)
			if  64 < ord(deCode[i]) < 68 or 96 < ord(deCode[i]) < 100:
				enCode += chr(ord(deCode[i]) + 23)
			else:
				enCode += chr(ord(deCode[i]) - 3)
		print('Decrypted string: ',enCode);
	else:
		print('You must enter only letters');

def encrypt(plaintext, key):
	abc = 'abcdefghijklmnopqrstuvwxyz'
	text_encrypt = ''
	i = 0
	for letra in plaintext:
		sum = abc.find(letra) + abc.find(key[i % len(key)])
		node = int(sum) % len(abc)
		text_encrypt = text_encrypt + str(abc[node])
		i = i + 1
	return text_encrypt

def decrypt(plaintext, key):
	abc = 'abcdefghijklmnopqrstuvwxyz'
	text_encrypt = ''
	i = 0
	for letra in plaintext:
		sum = abc.find(letra) - abc.find(key[i % len(key)])
		node = int(sum) % len(abc)
		text_encrypt = text_encrypt + str(abc[node])
		i = i + 1
	return text_encrypt

if __name__ == '__main__':
	encrypt_caesar(str(input('Encrypted: ')))
	decrypt_caesar(str(input('Decrypted: ')))
	print(encrypt(str(input('plaintext a encrypt: ')).lower(), str(input('key: ')).lower()))
	print(decrypt(str(input('plaintext a desencrypt: ')).lower(), str(input('key: ')).lower()))
