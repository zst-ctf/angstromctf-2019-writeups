# High Quality Checks
Rev

## Challenge 

After two break-ins to his shell server, kmh got super paranoid about a third! He's so paranoid that he abandoned the traditional password storage method and came up with this monstrosity! I reckon he used the flag as the password, can you find it?

Author: Aplet123

## Solution

Decompile in Ghidra


Cleaned up slightly

	undefined8 main(void){
	  puts("Enter your input:");
	  __isoc99_scanf(&DAT_00400b96,local_28);
	  if (strlen(local_28) < 0x13) {
	    puts("Flag is too short.");
	  }else {
	    iVar1 = check(local_28);
	    if (iVar1 == 0) {
	      puts("That\'s not the flag.");
	    }
	    else {
	      puts("You found the flag!");
	    }
	  }
	}

	undefined8 check(char *pcParm1){
		int iVar1 = d(pcParm1 + 0xc);

		bool all_checks = 
			d(pcParm1[0xc]) != 0 &&
			v(pcParm1[0x00]) != 0 &&
			u(pcParm1[0x10], pcParm1[0x11]) != 0 &&

			k(pcParm1[5]) == 0 &&
			k(pcParm1[9]) == 0 &&
			w(pcParm1[1]) != 0 &&
			b(pcParm1, 0x12) != 0 &&
			b(pcParm1, 0x4) != 0 &&
			z(pcParm1, 0x6c) != 0 &&
			s(pcParm1) != 0;

		return all_checks;
	}

Within check, there are more functions

[decompiled.c](decompiled.c)

Let's go through each check

#### Part 1: For `d(pcParm1[0xc]) != 0`:

It is a direct comparison, get the string directly

	>>> p32(0x30313763)
	'c710'

#### Part 2: For `v(pcParm1[0x00]) != 0`:

Function code

	ulong v(byte bParm1){
		return (bParm1 ^ 0x37) == (0xAC >> 1) );
	}

Direct comparison again 

	>>> chr((0xAC >> 1) ^ 0x37)
	'a'

#### Part 3: For `u(pcParm1[0x10], pcParm1[0x11]) != 0`:

Function code

	undefined8 u(char cParm1,char cParm2){
	  int iVar1 = n(0xdc);
	  if (((int)cParm1 == iVar1) && (iVar1 = o((ulong)(uint)(int)cParm2), iVar1 == 0x35053505)) {
	    return 1;
	  }
	  return 0;
	}

	ulong o(char cParm1) {	  
	  if (cParm1 < 'a') {
	    local_c = (int)cParm1 + -0x30;
	  }
	  else {
	    local_c = (int)cParm1 + -0x57;
	  }
	  local_c = (int)cParm1 * 0x100 + local_c;
	  return (ulong)(uint)(local_c * 0x10001);
	}

2 chars are compared. We get this for the first.

	>>> chr(0xDC >> 1)
	'n'

For the second, we first divide back by 0x10001.

	>>> hex(0x35053505 / 0x10001)
	'0x3505'

Then realised that the original char has a 0x100 multiplied. We can discard the lower byte.

	>>> (0x35053505 / 0x10001) // 0x100
	53
	>>> chr((0x35053505 / 0x10001) // 0x100)
	'5'

#### Part 4: For `k(pcParm1[5]) == 0` and `k(pcParm1[9]) == 0`:

Function code

	ulong k(char cParm1){
	  int iVar1 = o((ulong)(uint)(int)cParm1);
	  return (ulong)(iVar1 != 0x660f660f);
	}

Similar to previous Part 3...

	>>> chr((0x660f660f / 0x10001) // 0x100)
	'f'

#### Part 5: For `w(pcParm1[1]) != 0`:

Function code

	ulong w(char *pcParm1){
	  return (ulong)((int)*pcParm1 + (int)pcParm1[2] * 0x10000 + 
	  	(int)pcParm1[1] * 0x100 == 0x667463);
	}

Three chars being compared. They are multiplied by 0x1, 0x100 and 0x10000 respectively.

Hence, they are in sequence of `[2][1][0]`...

	Chars are 
	0x63, 0x74, 0x66

#### Part 6: For `b(pcParm1, 0x12) != 0` and `b(pcParm1, 0x4) != 0`:

Function code

	ulong b(long lParm1,uint uParm2){
	  cVar1 = *(char *)(lParm1 + uParm2);
	  iVar2 = n(0xf6); 
	  iVar3 = e((ulong)uParm2);
	  return (cVar1 == iVar3 * 2 + iVar2);
	}

	// shift down by 1, but retain sign
	ulong e(int iParm1){
	  uint uVar1;
	  
	  uVar1 = (uint)(iParm1 >> 0x1f) >> 0x1e;
	  uVar1 = (iParm1 + uVar1 & 3) - uVar1;
	  return (ulong)(uint)((int)(uVar1 + (uVar1 >> 0x1f)) >> 1);
	}


Simplifying it...

	flag[0x12] == chr( ( ((0x12 & 3) >> 1) * 2 + (0xf6 >> 1)) )
	flag[0x4]  == chr( ( ((0x4 & 3) >> 1) * 2 + (0xf6 >> 1)) )

We get the char

	>>> chr( ( ((0x12 & 3) >> 1) * 2 + (0xf6 >> 1)) )
	'}'
	>>> chr( ( ((0x4 & 3) >> 1) * 2 + (0xf6 >> 1)) )
	'{'

Similarly


#### Part 7: For `z(pcParm1, 0x6c)`:


Function code (heavily refactored)

	undefined8 z(long lParm1,char cParm2){
	  char cVar1;
	  char local_17 = 0;
	  char local_16 = 0;

	  for (uint local_14 = 0; local_14 < 8; local_14++) {
	  	// remove get bit at position
	    cVar1 = (char)(((int)cParm2 & 1 << ((byte)local_14 & 0x1f)) >> ((byte)local_14 & 0x1f));
	    
	    if ((local_14 & 1) == 0) { // for odd bits
	      local_16 +=  (char) (cVar1 << ((local_14) / 2));
	    }
	    else {
	      local_17 +=  (char) (cVar1 << ((local_14) / 2));
	    }
	  }

	  return 
	  	lParm1[local_17] == 'u' &&
	  	lParm1[local_17 + 1] == (0xdc >> 1) &&
	  	lParm1[local_16] == (0xea >> 1) &&
	  	lParm1[local_16 + 1] == 'n';
	}

Since `cParm2` is fixed at `0x6c`, we can precalculate the `local_17` and `local_16`

	cParm2 = 0b01101100

	// Even bits
	local_17 = 0b0_1_1_0_
	local_17 = 6

	// Odd bits
	local_16 = 0b_1_0_1_0
	local_16 = 10

Hence

	local_16 = 10
	local_17 = 6
	flag[local_17] == 'u' &&
	flag[local_17 + 1] == (0xdc >> 1) &&
	flag[local_16] == (0xea >> 1) &&
	flag[local_16 + 1] == 'n';


#### Part 8: For `s(pcParm1) != 0`:

Function code (refactored heavily)

	ulong s(long lParm1){
	  int iVar1;
	  int local_10 = 0;

	  for (int local_c = 0; local_c < 0x13; local_c++) {
	    iVar1 = o((ulong)(uint)(int)*(char *)(lParm1 + (long)local_c));
	    if (iVar1 == 0x5f2f5f2f) {
	      local_10 = local_10 + local_c + 1;
	    }
	  }
	  return (ulong)(local_10 == 9);
	}

Code simply iterates through the function and checks if index 9 (one-indexed) is equal to result of `o() == 0x5f2f5f2f`
Similar to previous Part 3...

	# flag[9-1]
	>>> chr((0x5f2f5f2f / 0x10001) // 0x100)
	'_'

#### Finally get the flag

	$ python3 flag.py 
	['a', 'c', 't', 'f', '{', 'f', 'u', 'n', '_', 'f', 'u', 'n', 'c', '7', '1', '0', 'n', '5', '}']
	actf{fun_func710n5}

## Flag

	actf{fun_func710n5}
