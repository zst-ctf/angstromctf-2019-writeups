undefined8 main(int iParm1,undefined8 *puParm2){
  time_t tVar1;
  
  if (iParm1 != 3) {
    printf("USAGE: %s in.png out.png\n",*puParm2);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  read_file(puParm2[1]);
  encode();
  write_file(puParm2[2]);
  return 0;
}

void encode(void)

{
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
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  lVar4 = 0x20;
  puVar5 = local_118;
  while (lVar4 != 0) {
    lVar4 = lVar4 + -1;
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  printf("message (less than 256 bytes): ");
  fgets((char *)local_118,0x100,stdin);
  local_140 = 0;
  while (local_140 < 0x100) {
    lVar4 = *(long *)(rows + (long)local_140 * 8);
    local_13c = 0;
    while (local_13c < 0x100) {
      pbVar3 = (byte *)(lVar4 + (long)(local_13c * 3));
      iVar2 = rand();
      *pbVar3 = (byte)iVar2 & 1 ^ *pbVar3;
      iVar2 = rand();
      pbVar3[1] = pbVar3[1] ^ (byte)iVar2 & 1;
      iVar2 = rand();
      pbVar3[2] = pbVar3[2] ^ (byte)iVar2 & 1;
      local_13c = local_13c + 1;
    }
    local_138 = 0;
    while (local_138 < 8) {
      pbVar3 = (byte *)(lVar4 + (long)(local_138 * 0x60));
      cVar1 = *(char *)((long)local_118 + (long)local_140);
      if ((pbVar3[2] & 1) != 0) {
        pbVar3[2] = pbVar3[2] ^ 1;
      }
      pbVar3[2] = pbVar3[2] |
                  (byte)((int)cVar1 >> ((byte)local_138 & 0x1f)) & 1 ^ (pbVar3[1] ^ *pbVar3) & 1;
      local_138 = local_138 + 1;
    }
    local_140 = local_140 + 1;
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
