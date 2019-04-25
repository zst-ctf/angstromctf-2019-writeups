# Powerball
Crypto

## Challenge 

Introducing ångstromCTF Powerball, where the Grand Prize is a flag! All you need to do is guess 6 ball values, ranging from 0 to 4095. But don't worry, we'll give one for free!

nc crypto.2019.chall.actf.co 19001

Author: defund

powerball.zip

## Hint

This oblivious transfer protocol is straight from Wikipedia!


## Solution

From the code, it looks like some sort of RSA protocol

    self.write(welcome)
    balls = [getRandomRange(0, 4096) for _ in range(6)]
    x = [getRandomRange(0, n) for _ in range(6)]
    self.write('x: {}\n'.format(x).encode())
    v = int(self.query(b'v: '))
    m = []
    for i in range(6):
        k = pow(v-x[i], d, n)
        m.append((balls[i]+k) % n)
    self.write('m: {}\n'.format(m).encode())
    guess = []
    for i in range(6):
        guess.append(int(self.query('Ball {}: '.format(i+1).encode())))
    if balls == guess:
        self.write(b'JACKPOT!!!')
        self.write(flag)
    else:
    
Looking at the hint, we go to Wikipedia and realise it is a 1-2 oblivious transfer protocol.

It is also called 1-out-of-2 oblivious transfer protocol using RSA blinding.

#### 1–2 oblivious transfer

- https://en.wikipedia.org/wiki/Oblivious_transfer
- http://zoo.cs.yale.edu/classes/cs467/2013s/lectures/ln23.pdf
- https://crypto.stackexchange.com/a/8862

This is the implementation.

    # 1. Alice has two messages, m0, m1, and wants to send exactly one of 
    # them to Bob. Bob does not want Alice to know which one he receives.

    # 2. Alice generates an RSA key pair, comprising the modulus N, 
    # the public exponent e and the private exponent d.

    # 3. She also generates two random values, x0, x1 and sends them to Bob 
    # along with her public modulus and exponent.

    # 4. Bob picks b to be either 0 or 1, and selects either the first or second xb.

    # 5. He generates a random value k and blinds xb by
    # computing v=(xb + k^e) mod N, which he sends to Alice.

    # 6. Alice doesn't know (and hopefully cannot determine) which of x0 and x1 Bob chose.
    # She applies both of her random values and comes up with two possible values for k:
    #     k0 =(v-x0)^d mod N and k1 =(v-x1)^d mod N
    # One of these will be equal to k and can be correctly decrypted by Bob (but not Alice),
    # while the other will produce a meaningless random value that does not reveal any 
    # information about k.

    # 7. She combines the two secret messages with each of the possible keys, 
    # m'0=m0+k0 and m'1=m1+k1, and sends them both to Bob.

    # 8. Bob knows which of the two messages can be unblinded with k, so he is able to compute exactly one of the messages m0=m'0-k0 and m1=m'1-k1.

From this, I extracted a few equations.

    All these in modulo N

    // Sending choice, b, to alice
    v  = (xb + k^e)
    k0 = (v-x0)^d
    k0 = ((xb + k^e)-x0)^d
    k0 = ((xb-x0 + k^e)^d

    If xb=x0 Then
        k0 = k

    // Bob unblinding messages
    # m'0 = m0 + k

How do we extract the other messages?

If you look carefully, the size of `m` (balls) is very small. It is only within 0 to 4096

    balls = [getRandomRange(0, 4096) for _ in range(6)]

After some thinking, the fastest method is to do a forward bruteforce and compare results.

Bruteforce technique

    I have m'1=m1+k1
    
    Since 0 <= m1 <= 4096,
    there are 4096 possibilities of k1
    
    Given k1 = (xb-x1 + k^e)^d,
    Find k1^e = (xb-x1 + k^e)^ed
         k1^e = (xb-x1 + k^e)    ---------- (Eqn 1)

    From Alice's message calculate k1^e also
         m'1=m1+k1
         k1 = m'1 - m1, where m1 is bruteforced
         k1^e = (m'1 - m1)^2     ---------- (Eqn 2)

    With (Eqn 1) and (Eqn 2) find the one that matches
    and that will be the correct m.

Final script: [solve.py](solve.py)

    $ python3 solve.py 
    Received: ************  ANGSTROMCTF POWERBALL  ************
    Correctly guess all 6 ball values ranging from 0
    to 4095 to win the jackpot! As a special deal,
    we'll also let you secretly view a ball's value!

    x: ...

    v: ...

    Found m[0] = 3012
    Found m[1] = 3825
    Found m[2] = 422
    Found m[3] = 3160
    Found m[4] = 3217
    Found m[5] = 2867
    Received: Ball 1:
    Received: Ball 2:
    Received: Ball 3:
    Received: Ball 4: Ball 5: Ball 6: JACKPOT!!!
    actf{no_more_free_oblivious_transfers}

## Flag

    actf{no_more_free_oblivious_transfers}
