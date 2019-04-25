#!/usr/bin/env python3
encrypted = [
    8930, 15006, 8930, 10302, 11772, 13806, 13340, 11556, 12432,
    13340, 10712, 10100, 11556, 12432, 9312, 10712, 10100, 10100,
    8930, 10920, 8930, 5256, 9312, 9702, 8930, 10712, 15500, 9312
]

reorder = [
    19, 4, 14, 3, 10, 17, 24, 22, 8, 2,
    5, 11, 7, 26, 0, 25, 18, 6, 21, 23,
    9, 13, 16, 1, 12, 15, 27, 20
]

# decrypt
decrypted = ''
for enc in encrypted:
    for ch in range(0xFF):
        if enc == ch*(ch-1):
            decrypted += chr(ch)
print(decrypted)

# reverse reorder
flag = [''] * 30
for old_i, new_i in enumerate(reorder):
    flag[new_i] = decrypted[old_i]

flag = ''.join(flag)
print(flag)

