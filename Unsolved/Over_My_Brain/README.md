# Over My Brain
Binary

## Challenge 

Everyone knows I'm in over my brain, over my brain ... with this esolang. With eight seconds left in overtime, it's on your mind, it's on your mind ... the source, of course!

/problems/2019/over_my_brain/

nc shell.actf.co 19010

Author: defund, lamchcl

## Solution

https://fatiherikli.github.io/brainfuck-visualizer/

https://en.wikipedia.org/wiki/Brainfuck#Commands

Address

	$ objdump -D over_my_brain | grep flag: -1
	flag:
	  4011c6:	55 	pushq	%rbp

Test

	          this loop through 256 cells and the stop at the 257th one
	+         set first to one
	[
	  [>+<-]  increment next one and then decrement current
	  >       go to next one again
	  .       print out (optional)
	  +       and increment next again
	]         stop when current is zero (next == current) 

	+[[>+<-]>+]++

Fuzz for address

	root@zst_ctf:/FILES # echo '+[[>+<-]>+]>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.' | ./over_my_brain | xxd

Working

	root@zst_ctf:/FILES # echo '+[[>+<-]>+.]' | ./over_my_brain | xxd
	00000000: 656e 7465 7220 736f 6d65 2062 7261 696e  enter some brain
	00000010: 6620 636f 6465 3a20 0203 0405 0607 0809  f code: ........
	00000020: 0a0b 0c0d 0e0f 1011 1213 1415 1617 1819  ................
	00000030: 1a1b 1c1d 1e1f 2021 2223 2425 2627 2829  ...... !"#$%&'()
	00000040: 2a2b 2c2d 2e2f 3031 3233 3435 3637 3839  *+,-./0123456789
	00000050: 3a3b 3c3d 3e3f 4041 4243 4445 4647 4849  :;<=>?@ABCDEFGHI
	00000060: 4a4b 4c4d 4e4f 5051 5253 5455 5657 5859  JKLMNOPQRSTUVWXY
	00000070: 5a5b 5c5d 5e5f 6061 6263 6465 6667 6869  Z[\]^_`abcdefghi
	00000080: 6a6b 6c6d 6e6f 7071 7273 7475 7677 7879  jklmnopqrstuvwxy
	00000090: 7a7b 7c7d 7e7f 8081 8283 8485 8687 8889  z{|}~...........
	000000a0: 8a8b 8c8d 8e8f 9091 9293 9495 9697 9899  ................
	000000b0: 9a9b 9c9d 9e9f a0a1 a2a3 a4a5 a6a7 a8a9  ................
	000000c0: aaab acad aeaf b0b1 b2b3 b4b5 b6b7 b8b9  ................
	000000d0: babb bcbd bebf c0c1 c2c3 c4c5 c6c7 c8c9  ................
	000000e0: cacb cccd cecf d0d1 d2d3 d4d5 d6d7 d8d9  ................
	000000f0: dadb dcdd dedf e0e1 e2e3 e4e5 e6e7 e8e9  ................
	00000100: eaeb eced eeef f0f1 f2f3 f4f5 f6f7 f8f9  ................
	00000110: fafb fcfd feff 00                        .......


52 offset

	echo '+[[>+<-]>+] >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >> .>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.' | ./over_my_brain | xxd

???

	echo '+[[>+<-]>+] >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>> >> >>>>>>>> >>>>>>>> >>>>>>>> >>>>>>>>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.' | ./over_my_brain | xxd

## Flag

	??