#!/usr/bin/env ruby
require 'openssl'

def invmod(e, et)
  e.to_bn.mod_inverse(et)
end

def powmod(x, e, n)
  x.to_bn.mod_exp(e, n)
end

def hex2ascii(text)
  [text].pack('H*')
end

# Encryption: public key
n = 99157116611790833573985267443453374677300242114595736901854871276546481648883
g = 99157116611790833573985267443453374677300242114595736901854871276546481648884
c = 2433283484328067719826123652791700922735828879195114568755579061061723786565164234075183183699826399799223318790711772573290060335232568738641793425546869

# Factorised by factordb.com
p = 310013024566643256138761337388255591613
q = 319848228152346890121384041219876391791

# function L is defined as L(x) = (x-1) / n
def L(x, n)
	return ((x.to_i - 1) / n)
end

# Decryption: private key

# compute n = pq and lambda = lcm(p-1, q-1)
lamb = (p-1).lcm(q-1)

# mu = (L(g^lambda mod n^2))^-1 mod n
mu =  invmod( L( powmod(g, lamb, n*n) , n), n)

# Compute the plaintext message as: 
# m = L(c^lamda mod n^2) * mu mod n
msg = (L(powmod(c, lamb, n*n), n) * mu) % n

# integer to ascii
msg = msg.to_s(16)
plaintext = hex2ascii(msg)
puts plaintext
