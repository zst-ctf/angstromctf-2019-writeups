#!/usr/bin/env python3

import json
import string
import base64

def bxor(a1, b1):
    encrypted = [ (a ^ b) for (a, b) in zip(a1, b1) ]
    return bytes(encrypted)

def xor_block(block, a, b):
	start_index = block * 16
	end_index = start_index + 16
	return bxor(a[start_index:end_index], b[start_index:end_index])

def replace_block(original_full, replacement, block):
	start_index = block * 16
	end_index = start_index + 16
	return original_full[:start_index] + replacement + original_full[end_index:]

handle = string.ascii_lowercase
session = {
    'admin': False,
    'handle': handle
}

token = '1hE2zRYdRTR6KDxtYAtGLDQJ5qIFyYRr45/eDlJAOGSoYJQb2+mFXxYzaS3Ge3Nz8l+Jaev3kR/Ih3yUMcR2zmJfYklgewHLSDVfUuz1JIo='
known_plaintext = json.dumps(session).encode()
known_ciphertext = base64.b64decode(token)
modified_plaintext = known_plaintext.replace(b'false', b'true ')
print('original pt:', known_plaintext)
print('modified pt:', modified_plaintext)

keystream0 = xor_block(0, known_plaintext, known_ciphertext)
modified_block0 = xor_block(0, modified_plaintext, keystream0)
print('[0] keystream:', keystream0)
print('[0] modified block:', modified_block0)

modified_ciphertext = replace_block(known_ciphertext, modified_block0, 0)
print('modified ct:', modified_ciphertext)
payload = base64.b64encode(modified_ciphertext).decode()
print('payload:', payload)

