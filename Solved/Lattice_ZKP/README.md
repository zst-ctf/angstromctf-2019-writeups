# Lattice ZKP
Crypto

## Challenge 

I tried to make a zero knowledge proof, but something isn't right.

nc 54.159.113.26 19003

Author: defund

lattice_zkp.zip

## Hint
Where's my randomness?

## Solution

We are given a program using some lattice cryptography.
	
	$ nc 54.159.113.26 19003

	    __      __  __  _                    __       
	   / /___ _/ /_/ /_(_)_______     ____  / /______ 
	  / / __ `/ __/ __/ / ___/ _ \   /_  / / //_/ __ \
	 / / /_/ / /_/ /_/ / /__/  __/    / /_/ ,< / /_/ /
	/_/\__,_/\__/\__/_/\___/\___/    /___/_/|_/ .___/ 
	                                         /_/      
	Query until you are convinced that I know s, where
	b = A*s + e

	A*r + e: <truncated>
	[0] r
	[1] r+s
	Choice: 0
	r: <truncated>

#### Understanding Theory of LWE

The program is an implementation of a [Learning With Error](https://en.wikipedia.org/wiki/Learning_with_errors) problem with a discrete uniform distribution (normal distribution).

Zero Knowledge Proof (ZKP)
- https://en.wikipedia.org/wiki/Zero-knowledge_proof#Practical_examples

Theory on LWE and Lattice based cryptography
- https://slideplayer.com/slide/14436254/
- https://medium.com/asecuritysite-when-bob-met-alice/learning-with-errors-and-ring-learning-with-errors-23516a502406
- https://eprint.iacr.org/2015/938.pdf
- https://crypto.stackexchange.com/questions/58630/lwe-with-secret-matrix-reverse-lwe

Resources for Lattice attacks
- https://www.maths.ox.ac.uk/system/files/attachments/lattice-reduction-and-attacks.pdf
- https://pdfs.semanticscholar.org/82cd/ea03b7c31ad3cd35bb7eeb25f7cf429508de.pdf
- https://hyperelliptic.org/tanja/lc17/ascrypto/day3/slides/heninger.pdf
- https://www.maths.ox.ac.uk/system/files/attachments/sage-introduction.pdf
- https://crypto.stackexchange.com/questions/26169/how-to-generate-new-lwe-samples


#### Bypass all that

However, I soon realised that this is unnecessary to understand the theory. The hint tells us it is an issue of randomisation.

When decoding the DerSequence from the server, the values are always the same for different runs of my script.

This was when I realised that the "random" function did not have a different seed. (ie. the values are consistent across runs)

	public = lambda: np.random.randint(q, size=(n, n))
	secret = lambda: np.random.randint(q, size=n)
	error = lambda: np.rint(np.random.normal(0, sigma, n)).astype(int)

Hence, the solution is simply to query for `r` and `r+s` and then subtract to get `s`.

> [solution](solution)

## Flag

	actf{deep_into_that_darkness_learning_with_errors_goes}
