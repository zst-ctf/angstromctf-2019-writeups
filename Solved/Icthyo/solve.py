#!/usr/bin/env python3
from PIL import Image

filename = 'out.png'
im = Image.open(filename).convert('RGB')
pix = im.load()
width, height = im.size

msg = ''
for h in range(0, height):
    ch = ''
    for i in range(8):
        row = h
        col = i * (0x60//3)
        r, g, b = pix[col, row]

        bit = (b & 1) ^ (g & 1) ^ (r & 1)
        ch += str(bit)

    # note LSB retrieved first so reverse
    ch = ch[::-1]
    msg += chr(int(ch, 2))

print(msg)
