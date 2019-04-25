# Lithp
Misc

## Challenge 

My friend gave me this program but I couldn't understand what he was saying - what was he trying to tell me?

Author: fireholder

[lithp.lisp.txt](lithp.lisp.txt)

## Solution

The code

> [lithp.lisp.txt](lithp.lisp.txt)

I debugged the functions in an online compiler

- https://rextester.com/l/common_lisp_online_compiler

This is my understanding of the code

	function (whats-this x y)
	    - returns x*y

	function (multh plain)
		- plain is a list
	    - returns a list of -a*a, for each a in list.

	function (owo inpth)
		- reorder the list according to the index given at *reorder*

	function (enc plain)
		- calls (owo (multh plain))
		- remove the negative sign for each item in list
		- print flag

So I simply reversed the process in a script

	$ python3 solve.py 
	_{_fmvtlpthelpahee_i_Iac_h}a
	actf{help_me_I_have_a_lithp}

## Flag

	actf{help_me_I_have_a_lithp}
