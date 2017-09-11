
# This method is made only for the Latin alphabet and lower letter 



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

def main():
	print(encrypt(str(input('plaintext a encrypt: ')).lower(), str(input('key: ')).lower()))
	print(decrypt(str(input('plaintext a desencrypt: ')).lower(), str(input('key: ')).lower()))

main()