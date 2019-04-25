# Intro to Rev
Rev

## Challenge 

Many of our problems will require you to run Linux executable files (ELFs). This problem will help you figure out how to do it on our shell server. Use your credentials to log in, then navigate to /problems/2019/intro_to_rev. Run the executable and follow its instructions to get a flag!

Author: SirIan

## Solution


	team3573@actf:~$ cd /problems/2019/intro_to_rev
	team3573@actf:/problems/2019/intro_to_rev$ ls 
	flag.txt  intro_to_rev

	team3573@actf:/problems/2019/intro_to_rev$ ./intro_to_rev 
	Welcome to your first reversing challenge!

	If you are seeing this, then you already ran the file! Let's try some input next.
	Enter the word 'angstrom' to continue: 
	angstrom
	Good job! Some programs might also want you to enter information with a command line argument.

	When you run a file, command line arguments are given by running './introToRev argument1 argument2' where you replace each argument with a desired string.

	To get the flag for this problem, run this file again with the arguments 'binary' and 'reversing' (don't put the quotes).


	team3573@actf:/problems/2019/intro_to_rev$ ./intro_to_rev binary reversing
	Welcome to your first reversing challenge!

	If you are seeing this, then you already ran the file! Let's try some input next.
	Enter the word 'angstrom' to continue: 
	angstrom
	Good job! Some programs might also want you to enter information with a command line argument.

	When you run a file, command line arguments are given by running './introToRev argument1 argument2' where you replace each argument with a desired string.

	Good job, now go solve some real problems!
	actf{this_is_only_the_beginning}

## Flag

	actf{this_is_only_the_beginning}
