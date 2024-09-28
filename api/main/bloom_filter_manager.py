from copy import copy
import struct
from typing import Optional

from api.main.bloom_filter import BloomFilter


class BloomFilterManager:

    _FILE_NAME = "filter.bf"
    _HEADER_IDENTIFIER = "BPBF"  # bloom proof bloom filter
    _HEADER_FORMAT = "4sIQ"  # 4s (identifier), I (num hash functions), Q (number of bits in the bit array)

    def __init__(self):
        self.filter: BloomFilter = Optional[None]

    def new_filter(self, file: str):
        self.filter = BloomFilter.new(expected_elements=240000, false_positive_rate=0.1)

        with open(file) as f:
            for line in f:
                self.filter.insert(line.strip())

    def write_filter_to_file(self):
        # each byte has 8 bits, so we need to determine how many bits we need to pad the last byte with
        pad_amount = (8 - self.filter.bit_array_size % 8) % 8

        bits: [int] = copy(self.filter.bit_array)
        bits.extend([0] * pad_amount)
        byte_array = bytearray(bits)

        # encode identifier string to bytes as utf-8
        identifier = self._HEADER_IDENTIFIER.encode()

        with open(self._FILE_NAME, "wb") as f:
            # identifier, num hash funcs
            header = struct.pack(self._HEADER_FORMAT,
                                 identifier, self.filter.num_hash_funcs, self.filter.bit_array_size)
            f.write(header)
            f.write(byte_array)

    def read_filter_from_file(self) -> BloomFilter:
        with open(self._FILE_NAME, "rb") as f:
            # Read the file header
            header = f.read(struct.calcsize(self._HEADER_FORMAT))
            identifier, num_hash_funcs, bit_array_size = struct.unpack(self._HEADER_FORMAT, header)
            identifier = identifier.decode()

            print(f"Identifier: {identifier}, num hash funcs: {num_hash_funcs}, bit array size: {bit_array_size}")
            if not self.validate_file(identifier=identifier):
                raise Exception("File not a valid bloom filter file")

            bits = list(bytearray(f.read()))

            # chop off the padding
            bits = bits[0:bit_array_size]

            return BloomFilter.new_from_file(num_hash_funcs=num_hash_funcs,
                                             bit_array=bits)

    def validate_file(self, identifier: str) -> bool:
        return identifier == self._HEADER_IDENTIFIER
