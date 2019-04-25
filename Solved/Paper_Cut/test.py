#!/bin/bash

import re
import zlib

pdf = open("paper_cut.pdf", "rb").read()
#stream = re.compile(r'.*?FlateDecode.*?stream(.*?)endstream', re.S)
#stream = re.compile(r'.*?FlateDecode.*?stream(.*)', re.S)

stream = pdf.split(b'stream')[1]
z = zlib.decompressobj()
s = stream

final_got = b''
while True:
    try:
        #for s in [stream]:#.findall(pdf):
        s = s.strip(b'\r\n')
        #print(zlib.decompress(s))
        buf = z.unconsumed_tail
        if buf == b"":
            buf = s
        got = z.decompress(buf)
        if got == "":
            break
        final_got += got
    except zlib.error:
        break

print(final_got)

test = re.findall(br"\((.*?)\)", final_got)

print(b''.join(test))


test = re.findall(br" ([0-9\.]+?) ([0-9\.]+?) ([mlc])", final_got.split(b' sc', 1)[1])
print(test)

test = list(map(lambda xy: [float(xy[0]), float(xy[1])], test))

import numpy as np
from matplotlib import pyplot as plt

data = np.array(test)
x, y = data.T
plt.plot(x,y)
plt.show()

quit()


with open('hello.pdf', 'rb') as f:
    hello = f.read()
    starting = hello.split(b'stream', 1)[0] + b'stream'
    middle_old = hello.split(b'stream', 1)[1].split(b'endstream', 1)[0]
    ending = b'endstream' + hello.split(b'endstream', 1)[1]

print('len', len(middle_old))
middle = final_got.decode(errors='ignore').encode()
with open('out.pdf', 'wb') as f:
    starting = starting.replace(b'Length 7', b'Length 100000')
    f.write(pdf + ending)



quit()
for line in final_got.split(b'Tj'):
    print(line)
    '''
    try:
        print(zlib.decompress(s))
        print("")
    except:
        pass
    '''