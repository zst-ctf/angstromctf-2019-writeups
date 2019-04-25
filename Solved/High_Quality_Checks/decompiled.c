// Shift down by 1
ulong n(int iParm1){
  return (ulong)(uint)(iParm1 >> 1);
}

// ?
ulong e(int iParm1){
  uint uVar1;
  
  uVar1 = (uint)(iParm1 >> 0x1f) >> 0x1e;
  uVar1 = (iParm1 + uVar1 & 3) - uVar1;
  return (ulong)(uint)((int)(uVar1 + (uVar1 >> 0x1f)) >> 1);
}


ulong o(char cParm1)
{     
  if (cParm1 < 'a') {
    local_c = (int)cParm1 + -0x30;
  }
  else {
    local_c = (int)cParm1 + -0x57;
  }
  local_c = (int)cParm1 * 0x100 + local_c;
  return (ulong)(uint)(local_c * 0x10001);
}


// Logic functions

ulong d(int *piParm1){
    return (ulong)(*piParm1 == 0x30313763);
}

ulong v(byte bParm1){
    int iVar1;

    iVar1 = n(0xac);
    return (ulong)((int)(char)(bParm1 ^ 0x37) == iVar1);
}

undefined8 u(char cParm1,char cParm2){
  int iVar1 = n(0xdc);
  if (((int)cParm1 == iVar1) && (iVar1 = o((ulong)(uint)(int)cParm2), iVar1 == 0x35053505)) {
    return 1;
  }
  return 0;
}


ulong k(char cParm1){
  int iVar1 = o((ulong)(uint)(int)cParm1);
  return (ulong)(iVar1 != 0x660f660f);
}



ulong w(char *pcParm1){
  return (ulong)((int)*pcParm1 + (int)pcParm1[2] * 0x10000 + (int)pcParm1[1] * 0x100 == 0x667463);
}

ulong b(long lParm1,uint uParm2){
  char cVar1;
  int iVar2;
  int iVar3;
  
  cVar1 = *(char *)(lParm1 + (long)(int)uParm2);
  iVar2 = n(0xf6);
  iVar3 = e((ulong)uParm2);
  return (ulong)((int)cVar1 == iVar3 * 2 + iVar2);
}


undefined8 z(long lParm1,char cParm2){
  char cVar1;
  int iVar2;
  char local_17;
  char local_16;
  uint local_14;
  
  local_17 = 0;
  local_16 = 0;
  local_14 = 0;
  while ((int)local_14 < 8) {
    cVar1 = (char)(((int)cParm2 & 1 << ((byte)local_14 & 0x1f)) >> ((byte)local_14 & 0x1f));
    if ((local_14 & 1) == 0) {
      local_16 = local_16 +
                 (char)((int)cVar1 << ((byte)((int)(local_14 + (local_14 >> 0x1f)) >> 1) & 0x1f));
    }
    else {
      local_17 = local_17 +
                 (char)((int)cVar1 << ((byte)((int)(local_14 + (local_14 >> 0x1f)) >> 1) & 0x1f));
    }
    local_14 = local_14 + 1;
  }
  if ((((*(char *)(lParm1 + (long)local_17) == 'u') &&
       (cVar1 = *(char *)(lParm1 + (long)local_17 + 1), iVar2 = n(0xdc), (int)cVar1 == iVar2)) &&
      (cVar1 = *(char *)(lParm1 + (long)local_16), iVar2 = n(0xea), (int)cVar1 == iVar2)) &&
     (*(char *)(lParm1 + (long)local_16 + 1) == 'n')) {
    return 1;
  }
  return 0;
}


ulong s(long lParm1)

{
  int iVar1;
  int local_10;
  int local_c;
  
  local_10 = 0;
  local_c = 0;
  while (local_c < 0x13) {
    iVar1 = o((ulong)(uint)(int)*(char *)(lParm1 + (long)local_c));
    if (iVar1 == 0x5f2f5f2f) {
      local_10 = local_10 + local_c + 1;
    }
    local_c = local_c + 1;
  }
  return (ulong)(local_10 == 9);
}
