void encode(void){
    char cVar1;
    int iVar2;
    byte *pbVar3;
    long lVar4;
    undefined8 *puVar5;
    long in_FS_OFFSET;
    int local_140;
    int local_13c;
    int local_138;
    undefined8 local_118 [33];

    // init with empty byte first 0x20 of the buffer
    lVar4 = 0x20;
    puVar5 = local_118;
    while (lVar4 != 0) {
        lVar4 = lVar4 + -1;
        *puVar5 = 0;
        puVar5 = puVar5 + 1;
    }

    // get message
    printf("message (less than 256 bytes): ");
    fgets((char *)local_118,0x100,stdin);
    
    // for row in 0..255
    local_140 = 0;
    while (local_140 < 0x100) {
        lVar4 = *(long *)(rows + (long)local_140 * 8);
        
        // for col (lVar4) in 0..255 
        local_13c = 0;
        while (local_13c < 0x100) {
            pbVar3 = (byte *)(lVar4 + (long)(local_13c * 3));

            // xor random pixel bit to R, G, B
            iVar2 = rand();
            *pbVar3 = (byte)iVar2 & 1 ^ *pbVar3;
            iVar2 = rand();
            pbVar3[1] = pbVar3[1] ^ (byte)iVar2 & 1;
            iVar2 = rand();
            pbVar3[2] = pbVar3[2] ^ (byte)iVar2 & 1;
            local_13c = local_13c + 1;
        }

        // 
        local_138 = 0;
        while (local_138 < 8) {
            // get pixel at i*0x60
            pbVar3 = (byte *)(lVar4 + (long)(local_138 * 0x60));

            // get each char of message
            cVar1 = *(char *)((long)local_118 + (long)local_140);

            // LSB at i*0x60+2 is always 0 initially
            if ((pbVar3[2] & 1) != 0) {
                pbVar3[2] = pbVar3[2] ^ 1;
            }

            // Then add in our LSB
            pbVar3[2] = pbVar3[2] |
                                    (byte)((int)cVar1 >> ((byte)local_138 & 0x1f)) & 1 ^ (pbVar3[1] ^ *pbVar3) & 1;

            // Effective code: pbVar3[2] |= (cVar1 >> local_138) & 1 ^ (pbVar3[1] ^ pbVar3[0]) & 1 )
            local_138 = local_138 + 1;
        }
        

        local_140 = local_140 + 1;
    }
    return;
}

