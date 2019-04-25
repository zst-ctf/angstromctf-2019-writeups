#!/usr/bin/env python3

flag = ['?'] * 0x13

# Part 1
flag[0xc+0] = 'c'
flag[0xc+1] = '7'
flag[0xc+2] = '1'
flag[0xc+3] = '0'

# Part 2
flag[0] = chr((0xAC >> 1) ^ 0x37)  # func n()

# Part 3
flag[0x10] = chr(0xDC >> 1)  # func n()
flag[0x11] = chr((0x35053505 // 0x10001) // 0x100)  # func o()

# Part 4
flag[5] = chr((0x660f660f // 0x10001) // 0x100)  # func o()
flag[9] = chr((0x660f660f // 0x10001) // 0x100)  # func o()

# Part 5
flag[1+2] = chr(0x66)  # func w()
flag[1+1] = chr(0x74)  # func w()
flag[1+0] = chr(0x63)  # func w()

# Part 6
flag[0x12] = chr( ( ((0x12 & 3) >> 1) * 2 + (0xf6 >> 1)) )
flag[0x4]  = chr( ( ((0x4 & 3) >> 1) * 2 + (0xf6 >> 1)) )

# Part 7
local_16 = 10
local_17 = 6
flag[local_17] = 'u'
flag[local_17 + 1] = chr(0xdc >> 1)
flag[local_16] = chr(0xea >> 1)
flag[local_16 + 1] = 'n'

# Part 8
flag[9-1] = chr((0x5f2f5f2f // 0x10001) // 0x100)

print(flag)
print(''.join(flag))