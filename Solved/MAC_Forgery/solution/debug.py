from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
#from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from Crypto.Util.strxor import strxor
import binascii

from Crypto.Util.py3compat import *

# https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Util/Padding.py
def pad(data_to_pad, block_size, style='pkcs7'):
    """Apply standard padding.
    :Parameters:
      data_to_pad : byte string
        The data that needs to be padded.
      block_size : integer
        The block boundary to use for padding. The output length is guaranteed
        to be a multiple of ``block_size``.
      style : string
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    :Return:
      The original data with the appropriate padding added at the end.
    """

    padding_len = block_size-len(data_to_pad)%block_size
    if style == 'pkcs7':
        padding = bchr(padding_len)*padding_len
    elif style == 'x923':
        padding = bchr(0)*(padding_len-1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0)*(padding_len-1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding

def bxor(a1, b1):
    encrypted = [ (a ^ b) for (a, b) in zip(a1, b1) ]
    return bytes(encrypted)


split = lambda s, n: [s[i:i+n] for i in range(0, len(s), n)]

class CBC_MAC:

    BLOCK_SIZE = 16
    block_count = 0

    def __init__(self, key):
        self.key = key

    def next(self, t, m):
        print(f'\n[Block {self.block_count}] next({t}, {m})')
        print('strxor(t, m) ==', strxor(t, m).hex())
        #return AES.new(self.key, AES.MODE_CBC, t).encrypt(m)
        encrypted = AES.new(self.key, AES.MODE_ECB).encrypt(strxor(t, m))
        print('keystream ==', bxor(encrypted, m).hex())
        print('encrypted ==', encrypted.hex())

        return encrypted

    def mac(self, m, iv):
        m = pad(m, self.BLOCK_SIZE)
        print('pad(m):', m)
        m = split(m, self.BLOCK_SIZE)
        print('split(m):', m)
        m.insert(0, long_to_bytes(len(m), self.BLOCK_SIZE)) # number of blocks
        print('m.insert:', m)
        t = iv

        self.block_count = 0
        for i in range(len(m)):
            t = self.next(t, m[i])
            self.block_count += 1
        return t

    def generate(self, m):
        iv = get_random_bytes(self.BLOCK_SIZE)
        return iv, self.mac(m, iv)

    def generate_with_iv(self, m, iv):
        return iv, self.mac(m, iv)

    def verify(self, m, iv, t):
        return self.mac(m, iv) == t


flag = "test flag"
key = "test kez".zfill(16)
key = '\x00' * 16

welcome = b'''\
If you provide a message (besides this one) with
a valid message authentication code, I will give
you the flag.'''

cbc_mac = CBC_MAC(key)

def handle():
    iv, t = cbc_mac.generate(welcome)
    print('iv:', iv.hex())
    print('t :', t.hex())

    print("==================")
    print(welcome)
    print(b'MAC: %b' % binascii.hexlify(iv+t))


def test():
    my_msg = b'AAAAAAAAAAAAAAAA'
    my_msg = welcome

    iv, t = cbc_mac.generate(my_msg)
    print('my_msg:', my_msg)
    print('iv:', iv.hex())
    print('t :', t.hex())
    print("==================")


    bit_flip = b'\x00' * 15 + bxor(b'\x09', b'\x07') 
    iv = bxor(iv, bit_flip)
    my_msg += b'\x01'*1 ## append with our known last block padding
    # my_msg += b'\x01'*16 ## append with our known last block
    my_msg += t ## last CBCMAC to make it zeroed out

    # iv = bytes.fromhex('54c32ca3f9d0e97a6eb8ca7f31c124c2')
    iv, t = cbc_mac.generate_with_iv(my_msg, iv)
    print('my_msg:', my_msg)
    print('iv:', iv.hex())
    print('t :', t.hex())
    print("==================")
    final_keystream = bxor(t, b'\x10' * 16)
    print('final_keystream:', final_keystream)
    print('key:', key.encode())
    print('keystream ^ key:', bxor(final_keystream, key.encode()).hex())

def test2():
    my_msg = welcome

    iv, t = cbc_mac.generate(my_msg)
    print('my_msg:', my_msg)
    print('iv:', iv.hex())
    print('t :', t.hex())
    print("==================")

    BLOCK_SIZE = 16
    orig_block_len = (len(welcome) // BLOCK_SIZE) + 1
    #new_block_len = orig_block_len + 2
    new_block_len = orig_block_len + 2 + orig_block_len - 1

    orig_iv = iv

    # do a bit flip
    bit_flip = b'\x00' * 15 + bxor(bytes([orig_block_len]), bytes([new_block_len]))
    print('bit_flip', bit_flip)
    iv = bxor(iv, bit_flip)

    # append with our known last block padding
    my_msg += b'\x01'*1  ## Extra block 1
    

    ## we know last CBCMAC is equal to t
    ## manipulate it to our advantage to zero out
    #my_msg += t

    ## Instead of zeroing out, we can mannipulate it to make it
    ## be a carbon copy of our first block
    #m_raw = pad(welcome, BLOCK_SIZE)
    m_raw = welcome
    print('m_raw:', m_raw)
    m_raw = split(m_raw, BLOCK_SIZE)

    # prepend number of blocks
    ## do padding with one extra block since we are appending it later
    m_raw.insert(0, long_to_bytes(orig_block_len, BLOCK_SIZE)) 
    print('m_raw:', m_raw)

    strxor0 = strxor(m_raw[0], orig_iv)
    my_msg += bxor(t, strxor0)  ## Extra block 1

    ## Extra block 2 through 2+len(m_raw)-1
    for i in range(1, len(m_raw)):
        #strxorN = strxor(m_raw[i], m_raw[i-1]) 
        my_msg += m_raw[i]

    # iv = bytes.fromhex('54c32ca3f9d0e97a6eb8ca7f31c124c2')
    iv, t = cbc_mac.generate_with_iv(my_msg, iv)
    print('my_msg:', my_msg)
    print('iv:', iv.hex())
    print('t :', t.hex())
    print("==================")
    final_keystream = bxor(t, b'\x10' * 16)
    print('final_keystream:', final_keystream)
    print('key:', key.encode())
    print('keystream ^ key:', bxor(final_keystream, key.encode()).hex())


if __name__ == '__main__':
    #handle()
    test2()
