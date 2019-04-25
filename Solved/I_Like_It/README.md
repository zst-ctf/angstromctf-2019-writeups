# I Like It
Rev

## Challenge 

Now I like dollars, I like diamonds, I like ints, I like strings. Make Cardi like it please.

/problems/2019/i_like_it

Author: SirIan

## Solution

Decompile in Hopper

	int main(int arg0, int arg1) {
	    puts("I like the string that I'm thinking of: ");
	    fgets(&var_20, 0x14, *stdin@@GLIBC_2.2.5);
	    *(int8_t *)(rbp + (strlen(&var_20) - 0x1) + 0xffffffffffffffe0) = 0x0;
	    if (strcmp(&var_20, "okrrrrrrr") != 0x0) {
	            puts("Cardi don't like that.");
	            rax = exit(0x0);
	    }
	    else {
	            puts("I said I like it like that!");
	            puts("I like two integers that I'm thinking of (space separated): ");
	            fgets(&var_2C, 0xc, *stdin@@GLIBC_2.2.5);
	            __isoc99_sscanf(&var_2C, "%d %d", &var_34, &var_30);
	            if (((var_30 + var_34 == 0x88) && (var_30 * var_34 == 0xec7)) && (var_34 < var_30)) {
	                    puts("I said I like it like that!");
	                    printf("Flag: actf{%s_%d_%d}\n", &var_20, var_34, var_30);
	                    rax = 0x0;
	                    rcx = *0x28 ^ *0x28;
	                    if (rcx != 0x0) {
	                            rax = __stack_chk_fail();
	                    }
	            }
	            else {
	                    puts("Cardi don't like that.");
	                    rax = exit(0x0);
	            }
	    }
	    return rax;
	}

From the code we see that we need to put a string

	okrrrrrrr

And then 2 numbers which meet the conditions

	(var_30 + var_34 == 0x88)
	(var_30 * var_34 == 0xec7)
	(var_34 < var_30)

Using factordb.com, we get the factors

	3783 = 3 * 13 * 97

We eventually get the numbers

	39 and 97

Now put into the server

	$ ./i_like_it 
	I like the string that I'm thinking of: 
	okrrrrrrr
	I said I like it like that!
	I like two integers that I'm thinking of (space separated): 
	39 97
	I said I like it like that!
	Flag: actf{okrrrrrrr_39_97}

## Flag

	actf{okrrrrrrr_39_97}
