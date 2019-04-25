# Icthyo
Rev

## Challenge 

Long before stegosaurus roamed the earth, another species prowled the sea; here is an artist's rendition.

Author: defund

[icthyo](icthyo)

[out.png](out.png)

## Solution

#### Code operation

Decompiled in Ghidra: [decompiled.c](decompiled.c)

The main function takes the in.png and goes through encode() then produced out.png

libpng is used to handle the image file

Sample code to understand how libpng is used.

- https://gist.github.com/niw/5963798

#### Summary of encode() function

I had simplified the decompiled `encode()` function to my understanding here: [decompiled_simplified.c](decompiled_simplified.c)

- Goes through a pixel LSB randomisation (does not affect decryption)
- Each message char is stored in each row.
- Within each row, 8 bits of the char is stored as follows
	+ `pbVar3 = row[i*0x60]`
	+ `pbVar3[2] |= (cVar1 >> local_138) & 1 ^ (pbVar3[1] ^ pbVar3[0]) & 1 )`
	+ `pbVar3[2] & 1, aka. LSB at i*0x60+2, is always 0 initially`

- It is using libpng, which does indexing like this

	+ `RED   = pixel[x*3 + 0]`
	+ `GREEN = pixel[x*3 + 1]`
	+ `BLUE  = pixel[x*3 + 2]`

#### How to decrypt?

- For each row, get RGB groups at `i*0x60` where i = 0..7
- For each RGB group, decrypt bit by the following logic

Retrieve bits

	Rearrange
		pbVar3[2] |= (cVar1 >> i) & 1 ^ (pbVar3[1] ^ pbVar3[0]) & 1 )

	Hence
		bit = pbVar3[2]&1 ^ (pbVar3[1] ^ pbVar3[0])&1)
		bit = (blue&1) ^ (green&1) ^ (red&1)

	Note that bit is retrieved from LSB first

I put it all into a python3 script

	Icthyo $ python3 solve.py 
	actf{lurking_in_the_depths_of_random_bits}

## Flag

	actf{lurking_in_the_depths_of_random_bits}
