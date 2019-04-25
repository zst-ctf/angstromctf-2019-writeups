#!/usr/bin/env python3
from debug import *
import socket

welcome = b'''\
If you provide a message (besides this one) with
a valid message authentication code, I will give
you the flag.'''


def generate_payload(iv, t):
    my_msg = welcome

    # iv, t = cbc_mac.generate(my_msg)
    print('my_msg:', my_msg)
    print('iv:', iv.hex())
    print('t :', t.hex())
    print("==================")

    BLOCK_SIZE = 16
    orig_block_len = (len(welcome) // BLOCK_SIZE) + 1
    #new_block_len = orig_block_len + 2
    new_block_len = orig_block_len + 2 + orig_block_len - 1

    orig_iv = iv

    # welcome has 7 blocks, and we are appending X more blocks
    # do bit flip to keep initial keystream consistent
    bit_flip = b'\x00' * 15 + bxor(bytes([orig_block_len]), bytes([new_block_len]))
    print('bit_flip', bit_flip)
    iv = bxor(iv, bit_flip)

    # append with our known last block padding
    my_msg += b'\x01'*1  ## Extra block 1
    
    # The last cbc-mac will make N-1 block be equal to \x00
    # this will always produce a consistent encryption

    ## we know last CBCMAC is equal to t
    ## if we manipulate it to our advantage to zero out
    #my_msg += t

    ## Instead of zeroing out, we can manipulate it to make it
    ## be a carbon copy of our first block

    # from the aove we did this...
    # where CBC-MAC(m + pad + t) = CBC-MAC('\x00'*16)

    ## If we control it right, we will make a carbon copy such that
    # then CBC-MAC(m + pad + m') = CBC-MAC(m)

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

    return (my_msg, iv.hex() + t.hex())


if __name__ == '__main__':
    s = socket.socket()
    s.connect(('crypto.2019.chall.actf.co', 19002))

    while True:
        data = s.recv(4096).decode().strip()
        if not data:
            break
        print("Received:", data)

        if 'actf' in data:
            quit()

        if 'MAC: ' in data:
            mac = data.split(':')[1].replace('Message', '').strip()
            print('Received IV >>', mac[:32])
            print('Received T >>', mac[32:])
            iv = bytes.fromhex(mac[:32])
            t = bytes.fromhex(mac[32:])

            my_msg, new_mac = generate_payload(iv, t)
            message = my_msg.hex().encode()
            print('Sending message >>', message)
            print('Sending MAC >>', new_mac)
            s.send(message + b'\n')
            s.send(new_mac.encode() + b'\n')

