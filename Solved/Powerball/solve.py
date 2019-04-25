#!/usr/bin/env python3
import socket
from ast import literal_eval


if __name__ == '__main__':
	LOCAL_SERVER = False

	s = socket.socket()
	if LOCAL_SERVER:
		s.connect(('127.0.0.1', 3000))
	else:
		s.connect(('crypto.2019.chall.actf.co', 19001))

	# 1. Alice has two messages, m0, m1, and wants to send exactly one of 
	# them to Bob. Bob does not want Alice to know which one he receives.

	# 2. Alice generates an RSA key pair, comprising the modulus N, 
	# the public exponent e and the private exponent d.
	if LOCAL_SERVER:
		# I am debugging with a different key than the server key
		with open('./mypowerball-debug/public.txt') as f:
			n = int(f.readline()[3:])
			e = int(f.readline()[3:])
	else:
		# Actual server key
		n = 24714368843752022974341211877467549639498231894964810269117413322029642752633577038705218673687716926448339400096802361297693998979745765931534103202467338384642921856548086360244485671986927177008440715178336399465697444026353230451518999567214983427406178161356304710292306078130635844316053709563154657103495905205276956218906137150310994293077448766114520034675696741058748420135888856866161554417709555214430301224863490074059065870222171272131856991865315097313467644895025929047477332550027963804064961056274499899920572740781443106554154096194288807134535706752546520058150115125502989328782055006169368495301
		e = 65537

	# 3. She also generates two random values, x0, x1 and sends them to Bob 
	# along with her public modulus and exponent.

	### Retrieve x array
	data = ''
	while ']' not in data:
		data += s.recv(1024).decode()
	print("Received:", data)

	x_array = data.split('x: ')[1].split('\n')[0]
	x_array = literal_eval(x_array)
	# print("Found x:", x_array)

	# 4. Bob picks b to be either 0 or 1, and selects either the first or second xb.
	b = 0
	xb = x_array[b]

	# 5. He generates a random value k and blinds xb by
	# computing v=(xb + k^e) mod N, which he sends to Alice.
	def generate_v(N, xb, ke):
		v = (xb + ke) % N
		return v

	k = 1337
	v = generate_v(n, xb, pow(k, e))
	s.send(str(v).encode() + b'\n')
	print("Send v >>", v)

	# 6. Alice doesn't know (and hopefully cannot determine) which of x0 and x1 Bob chose.
	# She applies both of her random values and comes up with two possible values for k:
	#     k0 =(v-x0)^d mod N and k1 =(v-x1)^d mod N
	# One of these will be equal to k and can be correctly decrypted by Bob (but not Alice),
	# while the other will produce a meaningless random value that does not reveal any 
	# information about k.

	data = ''
	while ']' not in data:
		data += s.recv(1024).decode()
	print("Received:", data)

	# 7. She combines the two secret messages with each of the possible keys, 
	# m'0=m0+k0 and m'1=m1+k1, and sends them both to Bob.
	m_array = data.split('m: ')[1].split('\n')[0]
	m_array = literal_eval(m_array)

	# 8. Bob knows which of the two messages can be unblinded with k,
	# so he is able to compute exactly one of the messages m0=m'0-k0 and m1=m'1-k1.
	mb = (m_array[b] - k) % n

	x0 = x_array[0]
	x1 = x_array[1]

	##########################
	# Debugging
	##########################
	if LOCAL_SERVER:
		with open('./mypowerball/private.txt') as f:
			d = int(f.readline()[3:])
		k1 = (pow(xb+k**e-x1, d, n)) % n 
		k1a = (pow(v-x1, d, n))
		m1 = (m_array[1] - k1a) % n 
		print('DEBUG>> k1:', k1)
		print('DEBUG>>k1a:', k1a)
		print('DEBUG>>m1:', m1)
		# quit()

	###############################
	## Attacking
	##############################
	def solve_for_m(xb, xN, mprime, k, e, n):
		"""
		there are 4096 possibilities of k1
		
		Given k1 = (xb-x1 + k^e)^d,
		Find k1^e = (xb-x1 + k^e)^ed
		     k1^e = (xb-x1 + k^e)    ---------- (Eqn 1)

		From Alice's message calculate k1^e also
		     m'1=m1+k1
		     k1 = m'1 - m1, where m1 is bruteforced
		     k1^e = (m'1 - m1)^2     ---------- (Eqn 2)
		"""
		kA_pow_e = (xb-xN + pow(k, e, n)) % n
		for mN in range(4096):
			kB_pow_e = pow(mprime - mN, e, n)

			if kA_pow_e == kB_pow_e:
				# print("Found", mN)
				return mN

		# print("No match")
		return None

	# Since 0 < m < 4096, search space is sufficiently small
	# Bruteforve for values of m
	mFound = []
	for index in range(0, 5+1):
		xN = x_array[index]
		mPrime = m_array[index]
		result = solve_for_m(xb, xN, mPrime, k, e, n)
		mFound.append(result)
		print(f"Found m[{index}] = {result}")

	# Submit to server
	for mN in mFound:
		s.send(str(mN).encode() + b'\n')

	# Wait for flag
	while True:
		data = s.recv(40960).decode().strip()
		if not data:
			break
		print("Received:", data)

		if 'actf' in data:
			quit()

