# Classy Cipher
Crypto

## Challenge 

Every CTF starts off with a Caesar cipher, but we're [more classy.](classy_cipher.py)

Author: defund

## Solution

Similar to Ceasar cipher but it shifts the whole byte range of 0 to 255. 

We can bruteforce the shift.


```python
def encrypt(d, s):
	e = ''
	for c in d:
		e += chr((ord(c)+s) % 0xff)
	return e

for shift in range(256):
	flag = ':<M?TLH8<A:KFBG@V'
	decrypt = encrypt(flag, shift)
	if 'actf{' in decrypt:
		print(decrypt)
```

## Flag

	actf{so_charming}
