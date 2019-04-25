#!/bin/bash
import re
import zlib
from tkinter import *

pdf = open("paper_cut.pdf", "rb").read()

# Since we only have a truncated stream,
# the rest of the PDF is the stream
stream = pdf.split(b'stream')[1]
# stream = re.compile(r'.*?FlateDecode.*?stream(.*?)endstream', re.S)

# Decompress a partial zlib
# - https://stackoverflow.com/questions/20620374/how-to-inflate-a-partial-zlib-file
z = zlib.decompressobj()

retrieved = b''
while True:
    try:
        buf = z.unconsumed_tail
        if buf == b"":
            buf = stream.strip(b'\r\n')

        got = z.decompress(buf)
        if got == b"":
            break

        retrieved += got
    except zlib.error as e:
        break

# print(retrieved)

# Next, find all coordinates
# From inspection of the PDF, it appears after
# the sc command. Split it to make things easier
coord_str = retrieved.split(b' sc', 1)[1]

# Prepare canvas to draw coordinate points
root = Tk()
root.title("Angstrom CTF 2019")
cw = 1200 # canvas width
ch = 800 # canvas height
canvas_1 = Canvas(root, width=cw, height=ch, background="white")
canvas_1.grid(row=0, column=1)


# PDF Content Stream Operators
#    x_coord y_coord m
#    x_coord y_coord l
#    x1 y1 x2 y2 x3 y3 c
items = coord_str.decode().strip().replace('\n', ' ').split(' ')
print(items)

# Render it on the canvas
zoom_factor_x = 4.25
zoom_factor_y = 4
x_offset = 180
y_offset = 400
x_prev = 0
y_prev = 0
while len(items) > 0:
    operands = []


    while len(items) > 0:
        operands.append(items.pop(0))
        print(operands)
        if operands[-1] == 'm':
            # moveto
            x_prev = (float(operands[0]) - x_offset) * zoom_factor_x
            y_prev = (float(operands[1]) - y_offset) * zoom_factor_y
            break

        if operands[-1] == 'l':
            # lineto
            x_coord = (float(operands[0]) - x_offset) * zoom_factor_x
            y_coord = (float(operands[1]) - y_offset) * zoom_factor_y
            canvas_1.create_line(x_prev, ch-y_prev, x_coord, ch-y_coord)
            break

        if operands[-1] == 'c':
            # curveto
            x1 = (float(operands[0]) - x_offset) * zoom_factor_x
            y1 = (float(operands[1]) - y_offset) * zoom_factor_y
            x2 = (float(operands[2]) - x_offset) * zoom_factor_x
            y2 = (float(operands[3]) - y_offset) * zoom_factor_y
            x3 = (float(operands[4]) - x_offset) * zoom_factor_x
            y3 = (float(operands[5]) - y_offset) * zoom_factor_y
            x_prev = x3
            y_prev = y3
            canvas_1.create_line(x1, ch-y1, x2, ch-y2, x3, ch-y3, smooth="true")
            break

        if operands[-1] == 'f':
            # ignore fill
            break

# Show frame
root.mainloop()
