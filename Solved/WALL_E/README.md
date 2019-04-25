# WALL-E
Crypto

## Challenge 

My friend and I have been encrypting our messages using RSA, but someone keeps intercepting and decrypting them! Maybe you can figure out what's happening?

Author: lamchcl

wall-e.py
wall-e.txt

## Solution

#### Exponent is Small

Notice that the exponent is very small `e = 3`.

- https://crypto.stackexchange.com/a/6771

> Without padding, encryption of m is me mod n: the message m is interpreted as an integer, then raised to exponent e, and the result is reduced modulo n. If e = 3 and m is short, then m3 could be an integer which is smaller than n, in which case the modulo operation is a no-operation. In that case, you can just compute the cube root of the value you have (cube root for plain integers, not modular cube root).

So if our message is small enough, we can do a cube root to retrieve our message. 

Unfortunately, the message is padded.

---

#### Padding is using 0x00 bytes

However, it is padded with 0x00 bytes.

Let's say we do no padding

	c = m^e  [mod n]

If we do one padding of 1, we get this

	c = m1^e    [mod n]

	m1 = m * 0x100
	c = (m*0x100)^e    [mod n]
	
	Hence, by rearranging using exponent law:
	c = m^e * 0x100^e  [mod n]

So for multiples of paddings, we know that

	m1 = m * 0x100
	m2 = m * 0x100 * 0x100

	Thus, by the pattern...
	mP = m * 0x100^P, where P is the number of padding bytes

Because of the zero padding, we know that

	m % 0x100 == 0

	m = c^d mod n
	(c^d % n) % 0x100 == 0

#### Attacking...

So we know that we can divide away the padding. After which, check if the cube root operation is possible.

Since we are working with modulo N, the division must occur within the finite field.

---

I did a simple function to continuously add the modulo until the numerator is divisible.

	def divide_away_padding(numerator, n):
	    multiplicator = 0
	    while True:
	        #print('Iterate', multiplicator)
	        x = numerator + multiplicator * n
	        if (x & 0xFF) == 0:
	            x //= 0x100
	            break

	        multiplicator += 1
	    return (x, multiplicator)

To do it efficiently, I checked for the lowest byte to check if it equals to zero. This is because we are going to divide away a 0x00 byte, which means it is a multiple of 0x100 and hence ANDing with 0xFF will be equal to zero.

---

Despite this, there was no flag no matter how many times I divided.

Next, I realised that the cube root must be within the finite field too. 

This function simply does a cuberoot if possible. If not, it will add the modulo and check again. It does this for 10000 iterations (arbitary number) before it "times out"

	def cuberoot_under_modulo(orig, n):
	    for tries in range(10000):
	        result = gmpy2.iroot(orig, 3)[0]

	        if int(pow(result, 3)) == int(orig):
	            return result
	        else:
	            orig += n

---

Finally, looks like all the theory is going well.

Trying out, we get a success after a divison of 251 padding bytes.

	WALL_E $ python3 solve.py 
	Try padding: 0
	Try padding: 1
	Try padding: 2
	...
	Try padding: 250
	Try padding: 251
	b'actf{bad_padding_makes_u_very_sadding_even_if_u_add_words_just_for_the_sake_of_adding}'


## Flag

	actf{bad_padding_makes_u_very_sadding_even_if_u_add_words_just_for_the_sake_of_adding}
