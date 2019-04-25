import binascii
import numpy as np
import socketserver

from Crypto.Util.asn1 import DerSequence

import lwe


# b = A*s + e
with open('A.npy', 'rb') as f:
    A = np.load(f)

with open('b.npy', 'rb') as f:
    b = np.load(f)

print('A =', A)
print('b =', b)

def handle():
	r, b = lwe.sample(A)
	print(b'A*r + e:', (b))
	print(b'r:', (r))
	print(b'r+s:', (lwe.add(r, s)))

handle()
