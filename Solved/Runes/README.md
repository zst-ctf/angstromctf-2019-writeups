# Runes
Crypto

## Challenge 

The year is 20XX. ångstromCTF only has pwn challenges, and the winner is solely determined by who can establish a socket connection first. In the data remnants of an ancient hard disk, we've recovered a string of letters and digits. The only clue is the etching on the disk's surface: Paillier.

Author: defund

	n: 99157116611790833573985267443453374677300242114595736901854871276546481648883
	g: 99157116611790833573985267443453374677300242114595736901854871276546481648884
	c: 2433283484328067719826123652791700922735828879195114568755579061061723786565164234075183183699826399799223318790711772573290060335232568738641793425546869

## Solution

[Paillier cryptosystem](https://en.wikipedia.org/wiki/Paillier_cryptosystem)

Since n is factorised at factordb.com

	p = 310013024566643256138761337388255591613
	q = 319848228152346890121384041219876391791

We simply need to decrypt it. The equation is on the Wikipedia page

https://en.wikipedia.org/wiki/Paillier_cryptosystem#Decryption

I implemented Paillier decryption in Ruby script.

	$ ruby paillier_solve.rb 
	actf{crypto_lives}

## Flag

	actf{crypto_lives}
