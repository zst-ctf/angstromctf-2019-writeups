# Random ZKP
Crypto

## Challenge 
As the threat of quantum computing grows imminent, the world looks to a shining beacon of hope: lattice-based cryptography! Novel constructions abound, including this peculiar zero knowledge proof.

nc 54.159.113.26 19004

Author: defund

## Hint
Parameters taken from FrodoKEM and protocol inspired by discrete logarithms.

## Solution


https://people.csail.mit.edu/vinodv/6876-Fall2018/lecture2.pdf

https://eprint.iacr.org/2017/606.pdf

	BKW Another approach to solve LWE is based on the work from Blum, Kalai,
	and Wasserman [14], which was originally developed to solve the learning parity
	with noise problem. The main idea is to combine few LWE samples to get a new
	sample that depends only on a small part of the secret s. This part can then
	be recovered by brute-forcing all possibilities [5], or by advanced techniques like
	the multidimensional Fourier transform [22].

https://floriantramer.com/docs/slides/ecrypt15better.pdf
https://www.maths.ox.ac.uk/system/files/attachments/lattice-reduction-and-attacks.pdf

## Flag

	??