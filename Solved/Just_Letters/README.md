# Just Letters
Misc

## Challenge 

Hope you’ve learned the alphabet!

nc misc.2019.chall.actf.co 19600

Author: derekthesnake

https://esolangs.org/wiki/AlphaBeta

## Solution

It is an Esolang with instructions as alphabets.

When we connect to the server, we need to read a flag at memory zero.

	Welcome to the AlphaBeta interpreter! The flag is at the start of memory. You get one line:

Let's refer to the C++ interpreter, this is because the provided page is not so detailed.

https://github.com/TryItOnline/alphabeta/blob/master/AB.cpp

I will copy out the relevant instructions which we need to print the flag

#### Instructions

	// Set memory pointer to start, then put it
	// into Reg3 to be printed out to stdout

	if ( Program[Position] == "Y" ) { Register4[Mode] = 0 ;}
	if ( Program[Position] == "G" ) { Register1 = Memory[Register4[0]] ;}
	if ( Program[Position] == "C" ) { Register3 = Register1 ;}
	if ( Program[Position] == "L" ) { cout << char(Register3) ;}
	if ( Program[Position] == "S" ) { Register4[Mode] += 1 ;}

So we have YGCLS to print the first char

To print subsequent chars, we can repeat GCLS.

	YGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLS

It works, but it ain't fun and it is a hacky solution.

	$ nc misc.2019.chall.actf.co 19600
	Welcome to the AlphaBeta interpreter! The flag is at the start of memory. You get one line:
	> YGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLSGCLS
	actf{esolangs_sure_are_fun!}

---

Alternatively, let's do a loop

	// Set position pointer to start at index 1 of YCGLS = C

	if ( Program[Position] == "Z" ) { Mode = ( Mode + 1 ) % 2 ;}
	if ( Program[Position] == "Y" ) { Register4[Mode] = 0 ;}
	if ( Program[Position] == "S" ) { Register4[Mode] += 1 ;}
	if ( Program[Position] == "Z" ) { Mode = ( Mode + 1 ) % 2 ;}

	// Loop until a null char is reached

	if ( Program[Position] == "y" ) { Register2 = 0 ;}
	if ( Program[Position] == "O" ) { if ( Register1 != Register2 ) NewPosition = Register4[1];}

	  
We have the payloads...

Effectively, our code will loop and print each char, starting from memory zero, until a null byte is reached

	Y    # set memory pointer to zero
	CGL  # print the char at current memory [index 1]
	S    # increment to next memory pointer
	ZYSZ # Loop: setup by making position pointer to index 1
	yO	 # Loop: jump to position pointer of index 1 if current char is not a null byte.


Put to server

	$ nc misc.2019.chall.actf.co 19600
	Welcome to the AlphaBeta interpreter! The flag is at the start of memory. You get one line:
	> YCGLSZYSZyO
	actf{esolangs_sure_are_fun!}

## Flag

	actf{esolangs_sure_are_fun!}
