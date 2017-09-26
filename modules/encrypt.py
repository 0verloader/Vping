import os, random, struct, sys
from Crypto.Cipher import AES


def create_key(passw):
	length = len(passw)
	if length<16:
		for i in range(0,16-length):
			passw+="_"
	elif length<24:
		for i in range(0,24-length):
			passw+="_"
	elif length<32:
		for i in range(0,32-length):
			passw+="_"
	return passw


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


encrypt_file(key=create_key(sys.argv[1]),in_filename="test.txt")