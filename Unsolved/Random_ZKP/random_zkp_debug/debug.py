import binascii
import numpy as np
import socketserver

from Crypto.Util.asn1 import DerSequence

from lwe import *


# b = A*s + e
with open('A.npy', 'rb') as f:
    A = np.load(f)

with open('b.npy', 'rb') as f:
    bX = np.load(f)

print('A =', A)
print('b =', b)

def handle():
	s, b0 = sample(A)
	r, b1 = sample(A)
	print(b'A*r + e:', (b1))
	print(b'r:', (r))
	print(b'r+s:', (add(r, s)))

	e = b1 - mul(A, r)
	print('e[r]', e)
	e = b1 - mul(A, r+s)
	print('e[r+s]', e)
	print('s', s)

	print('A*s + e:', (b0))
	print('A(r+s) - (Ar + e)', add(mul(A, r+s), -b1))
	print('A(r+s) - (Ar)', add(mul(A, r+s), -1*mul(A, r)))
	print('A(r+s) - (Ar + e) - Ax', add(add(mul(A, r+s), -b1), -b0) )


	print('r+s:', (add(r, s)))

	'''
	sX, bX = sample(A)
	for x in range(100):
		sY, bY = sample(A)
		sX = add(sX, r+sY)
		bX = add(bX, r+bY)
	print('sX', sX)
	print('bX', bX)
	'''





handle()
