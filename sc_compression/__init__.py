from enum import Enum
import lzma
from typing import Optional

class Signature(Enum):
    NONE = 1
    LZMA = 2  # starts with 5D 00 00 04
    SC = 3  # starts with SC
    SCLZ = 4  # starts with SC and contains SCLZ
    SIG = 5  # starts with Sig:


class ScCompression:
    """
    This class can both compress and decompress Supercell game asset files. 

    Only fp OR buffer can be passed in, not both. 

    If fp is passed in, the file path must be valid.

    If a buffer is pased in, it must be from a valid Supercell game file.

    Parameters
    -----------
    fp : :class:`str` file path to read from
    buffer : :class:`bytes` bytes to read from
    """

    def __init__(self, fp: str = "", buffer: bytes = b"") -> None:
        if fp != "":
            self._fp = fp
            with open(self._fp, "rb") as _f:
                self._buffer = _f.read()
        elif buffer != b"":
            self._buffer = buffer
        else:
            raise ValueError("A file path or a buffer must be passed in.")

    def decompress(self) -> bytes:
        """
        Decompresses the buffer or file and returns the data back as bytes

        For data as a string, use :function:`decompress_to_str()` instead.

        As of now, LZHAM is unsupported, but might be in the future. 

        Returns
        --------
        :class:`bytes`
            Uncompressed data
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

    def decompress_to_str(self) -> str:
        """
        Decompresses the buffer or file and returns the data back as a string

        Returns
        --------
        :class:`str`
            Uncompressed data as a string
        """
        return self.decompress().decode("utf-8")

    def decompress_to_file(self, fp: str) -> int:
        """
        Compresses the data and writes it to a file.

        Parameters
        ----------
        fp : :class:`str`
            File path to write uncompressed data to

        Returns
        --------
        :class:`int`
            Number of bytes written to file
        """
        _bytes = self.decompress()
        with open(fp, "wb") as f:
            return f.write(_bytes)

    # do not access the functions below outside of the scope of this class

    def _decompressLZMA(self, offset: Optional[int] = 0) -> bytes:
        """
        Decompresses the data using the LZMA algorithm.

        Parameters
        ----------
        offset : :class:`Optional[int]` Index to start decompression at. Defaults to 0.

        Returns
        --------
        :class:`bytes` Uncompressed data
        """
        uncompressedSize = int.from_bytes(
            self._buffer[5+offset:9+offset], "big", signed=True)
        if uncompressedSize == -1:
            self._formattedbuffer = self._buffer[offset:9+offset] + \
                b"\xFF\xFF\xFF\xFF" + self._buffer[9+offset:]  # pack a -1
        else:
            self._formattedbuffer = self._buffer[offset:9+offset] + \
                b"\x00\x00\x00\x00" + self._buffer[9+offset:]  # pack a 0
        with open("newinsertpy.csv", "wb") as f:
            f.write(self._formattedbuffer)
        return lzma.decompress(self._formattedbuffer)

    def _decompressSC(self) -> bytes:
        """
        Decompresses the data using the LZMA algorithm but removes the 26 byte header (signature)

        Returns
        --------
        :class:`bytes` Uncompressed data
        """
        return self._decompressLZMA(26)

    def _decompressSCLZ(self) -> bytes:
        """
        TODO:

        Decompress the data using the LZHAM algorithm.
        """
        return self._buffer

    def _decompressSIG(self) -> bytes:
        """
        Decompresses the data using the LZMA algorithm but removes the 68 byte header (signature)

        Returns
        --------
        :class:`bytes` Uncompressed data
        """
        return self._decompressLZMA(68)

    def _readSignature(self) -> Signature:
        """
        Reads the signature of the buffer

        Returns
        --------
        :class:`Signature` Signature of the buffer
        """
        if self._buffer[:3].hex().lower() == "5d0000":
            return Signature.LZMA
        elif self._buffer[:2].decode("utf-8").lower() == "sc":
            if len(self._buffer) > 30 and self._buffer[26:30].decode("utf-8").lower() == "sclz":
                return Signature.SCLZ
            return Signature.SC
        elif self._buffer[:4].decode("utf-8").lower() == "sig:":
            return Signature.SIG
        return Signature.NONE
