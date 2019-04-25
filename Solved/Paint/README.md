# Paint
Crypto

## Challenge 

This amazing new paint protocol lets artists share secret paintings with each other! Good thing U.S. Patent 4200770 is expired.

Author: defund

[paint.py](paint.py)

[paint.txt](paint.txt)

## Solution

Diffie Hellman cryptography

- US patent 4200770, Hellman Diffie Merkle, public-key cryptography
- https://cr.yp.to/patents/us/4200770.html
- https://skerritt.blog/diffie-hellman-merkle/

---

Relevant equations:

	my_mix = pow(base, secret, palette)
	shared_mix = pow(your_mix, secret, palette)
	painting = image ^ shared_mix

We are given:

	palette
	base
	my_mix
	your_mix
	painting

We need to recover `secret` to get back the `image`.

---

First we notice is the modulus (`palette = 1 << 2048`) is non-prime.


- https://crypto.stackexchange.com/a/44786
- https://crypto.stackexchange.com/questions/67093/diffie-hellman-private-key-recover-with-non-prime-modulus?rq=1
- https://crypto.stackexchange.com/questions/30328/why-does-the-modulus-of-diffie-hellman-need-to-be-a-prime


The modulus is `1<<2048`. Hence, `palette = q^k` where `q = 2`, `k = 2048`

If g^a = 1 (mod q^k), then g^ab = 1 (mod q^k) so we have one solution to this subproblem.

- https://ctftime.org/task/6628

We can do a discrete log to get the secret easily. Using sage, it has a built-in function

	$ sage solve.sage 
	secret: 629921607003244034334739296597900783683872903809471621783318441724296155260647861566002145401774841786965516424821133148061140507283116747339148975177513485103967011207217568924993463569559551429141756952018711071204949930416859383037306197953684591391066287527469114753495090054370608519379326915615068308557735119497576999275516623932355604742058855833591651141407379343873413310424307672368844204423176033536465560324264458606570832918771689488513626547477988015235832957445514499444921298913651835294484177694907540420778298030233425343791552742606481998105977335541679798111463675261162481691943108104757462361
	message: actf{powers_of_two_are_not_two_powerful}

## Flag

	actf{powers_of_two_are_not_two_powerful}
