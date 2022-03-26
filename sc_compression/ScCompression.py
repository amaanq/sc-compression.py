from enum import Enum
import lzma
from typing import Optional


class Signature(Enum):
    NONE = 1
    LZMA = 2  # starts with 5D 00 00 04
    SC   = 3  # starts with SC
    SCLZ = 4  # starts with SC and contains SCLZ
    SIG  = 5  # starts with Sig:


class ScCompression:
    def __init__(self, fp: str = "", buffer: bytes = b"") -> None:
        """
        Only fp OR buffer can be passed in, not both. 

        `fp: file path to read from`
        `buffer: bytes to read from`
        """
        if fp != "":
            self._fp = fp
            with open(self._fp, "rb") as _f:
                self._buffer = _f.read()
        elif buffer != b"":
            self._buffer = buffer

    def Decompress(self) -> bytes:
        """
        Decompresses the buffer or file and returns the data back as bytes

        For data as a string, use DecompressToStr

        As of now, LZHAM is unsupported, but might be in the future. 
        """
        signature = self._readSignature()
        if signature == Signature.NONE:
            return self._buffer
        elif signature == Signature.LZMA:
            return self._decompressLZMA()
        elif signature == Signature.SC:
            return self._decompressSC()
        elif signature == Signature.SCLZ:
            return self._decompressSCLZ()
        elif signature == Signature.SIG:
            return self._decompressSIG()

    def DecompressToStr(self) -> str:
        """Decompresses the buffer or file and returns the data back as a string"""
        return self.Decompress().decode("utf-8")

    def DecompressToFile(self, fp: str) -> int:
        """Returns the number of bytes written"""
        _bytes = self.Decompress()
        with open(fp, "wb") as f:
            return f.write(_bytes)

    # do not access the functions below outside of the scope of this class

    def _decompressLZMA(self) -> bytes:
        uncompressedSize = int.from_bytes(
            self._buffer[5:9], "little", signed=True)
        if uncompressedSize == -1:
            self._formattedbuffer = self._buffer[:9] + \
                b"\xFF\xFF\xFF\xFF" + self._buffer[9:]  # pack a -1
        else:
            self._formattedbuffer = self._buffer[:9] + \
                b"\x00\x00\x00\x00" + self._buffer[9:]  # pack a 0
        return lzma.decompress(self._formattedbuffer)

    def _decompressSC(self) -> bytes:
        self._formattedbuffer = self._buffer[26:]
        return self._decompressLZMA()

    def _decompressSCLZ(self) -> bytes:
        self._formattedbuffer = self._buffer
        return self._formattedbuffer

    def _decompressSIG(self) -> bytes:
        self._formattedbuffer = self._buffer[68:]
        return self._decompressLZMA()

    def _readSignature(self) -> Signature:
        if self._buffer[:3].hex().lower() == "5d0000":
            return Signature.LZMA
        elif str(self._buffer[:2]).lower() == "sc":
            if len(self._buffer) > 30 and str(self._buffer[26:30]).lower() == "sclz":
                return Signature.SCLZ
            return Signature.SC
        elif str(self._buffer[:4]) == "sig:":
            return Signature.SIG
        return Signature.NONE
