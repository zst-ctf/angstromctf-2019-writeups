#!/usr/bin/env python3
import socket
import binascii
import telnetlib
import numpy as np
from Crypto.Util.asn1 import DerSequence
# requires pycryptodome
import otp
from lwe import *

# Reverse of pack
# pack = lambda x: binascii.hexlify(DerSequence(x.tolist()).encode())
def unpack(x):
    if len(x) % 2 == 1:
        x = '0' + x
    x = binascii.unhexlify(x)
    der = DerSequence()
    der.decode(x)
    return list(der)

def np_subtract(r_s, r):
    s = np.asarray(r_s) - r
    return np.mod(s, q)

def connect_server():
    s = socket.socket()
    s.connect(('54.159.113.26', 19004))
    t = telnetlib.Telnet()
    t.sock = s
    return t

with open('A.npy', 'rb') as f:
    A = np.load(f)

'''
with open('s.npy', 'rb') as f:
    s = np.load(f)
'''

if __name__ == '__main__':
    # Get b = A*r + e
    t = connect_server()

    print(t.read_until(b'A*r + e:').decode())
    b1 = t.read_until(b'\n').decode()
    print(b1)
    b1 = unpack(b1.strip())
    print(b1)

    # Get r
    t.write(b'0\n')

    print(t.read_until(b'r: ').decode())
    r = t.read_until(b'\n').decode()
    print(r)
    r = unpack(r.strip())
    print(r)


    # b1 = A*s + e
    # b1 - A*s = e
    e = b1 - mul(A, r)
    print('e', e)

    # (r+s)
    # A*(s+r) = As + Ar
    # b2 = Ar + e2
    # b0 = As + e0


    quit()
    '''
    print(t.read_until(b'r+s: ').decode())
    r_s = t.read_until(b'\n').decode()
    print(r_s)
    r_s = unpack(r_s.strip())
    print(r_s)
    '''
    


    # We have r+s, and r
    # s is our desired flag key
    #s = np_subtract(r_s, r)


    # decrypt using XOR cipher
    with open("flag.enc", 'rb') as f:
        enc = f.read()
        dec = otp.encrypt(s, enc)
        print(dec)
