"""This module cintains the function for decryption."""
import os
import struct
import sys
from Crypto.Cipher import AES


def create_key(passw):
    """Create an appopriate password."""
    length = len(passw)
    if length < 16:
        for i in range(0, 16 - length):
            passw += "_"
    elif length < 24:
        for i in range(0, 24 - length):
            passw += "_"
    elif length < 32:
        for i in range(0, 32 - length):
            passw += "_"
    return passw


def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):
    """ Decrypt a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip').
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


#decrypt_file(key=create_key(sys.argv[1]), in_filename="test.txt.enc")