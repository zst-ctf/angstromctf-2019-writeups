# One Bite
Rev

## Challenge 

Whenever I have friends over, I love to brag about things that I can eat in a single bite. Can you give this program a tasty flag that fits the bill?

/problems/2019/one_bite

Author: SirIan

## Solution

Decompile in Hopper

	int main(int arg0, int arg1) {
	    puts("Give me a flag to eat: ");
	    fgets(&var_40, 0x22, *__TMC_END__);
	    var_4C = 0x0;
	    while (sign_extend_64(var_4C) < strlen(&var_40)) {
	            *(int8_t *)(rbp + sign_extend_32(var_4C) + 0xffffffffffffffc0) = *(int8_t *)(rbp + sign_extend_32(var_4C) + 0xffffffffffffffc0) & 0xff ^ 0x3c;
	            var_4C = var_4C + 0x1;
	    }
	    if (strcmp(&var_40, "]_HZGUcHTURWcUQc[SUR[cHSc^YcOU_WA") == 0x0) {
	            puts("Yum, that was a tasty flag.");
	    }
	    else {
	            puts("That didn't taste so good :(");
	    }
	    rax = 0x0;
	    rcx = *0x28 ^ *0x28;
	    if (rcx != 0x0) {
	            rax = __stack_chk_fail();
	    }
	    return rax;
	}

From the code,

Flag goes through XOR cipher of `0x3c` and then gets compared to `"]_HZGUcHTURWcUQc[SUR[cHSc^YcOU_WA"`

Decrypt it

	$ python3

	>>> enc = b"]_HZGUcHTURWcUQc[SUR[cHSc^YcOU_WA"

	>>> dec = [chr(my_byte ^ 0x3c) for my_byte in enc]

	>>> ''.join(dec)
	'actf{i_think_im_going_to_be_sick}'

## Flag

	actf{i_think_im_going_to_be_sick}
