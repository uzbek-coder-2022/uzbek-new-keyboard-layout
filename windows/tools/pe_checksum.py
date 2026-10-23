#!/usr/bin/env python3
"""PE sarlavhasidagi CheckSum maydonini to'g'ri hisoblab yozadi (kernel yuklagichi uchun)."""
import struct
import sys


def pe_checksum(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    chk_off = pe + 4 + 20 + 64            # OptionalHeader.CheckSum (PE32 va PE32+ da bir xil)
    buf = bytearray(data)
    buf[chk_off:chk_off + 4] = b"\0\0\0\0"
    if len(buf) % 2:
        buf.append(0)
    total = 0
    for (w,) in struct.iter_unpack("<H", bytes(buf)):
        total += w
        total = (total & 0xFFFF) + (total >> 16)
    total = (total & 0xFFFF) + (total >> 16)
    return (total + len(data)) & 0xFFFFFFFF, chk_off


for path in sys.argv[1:]:
    with open(path, "rb") as fh:
        data = bytearray(fh.read())
    chk, off = pe_checksum(bytes(data))
    struct.pack_into("<I", data, off, chk)
    with open(path, "wb") as fh:
        fh.write(data)
    print("checksum: %s -> 0x%08X" % (path, chk))
