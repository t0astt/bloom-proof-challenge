from hashlib import md5
import math


class BloomFilter:
    """
    A probabilistic, memory-efficient structure for determining the likelihood of whether an element is contained
    within it.
    Reading material: https://en.wikipedia.org/wiki/Bloom_filter
    """

    def __init__(self, num_hash_funcs: int, bit_array: [int]):
        self.num_hash_funcs = num_hash_funcs
        self.bit_array = bit_array

        self.bit_array_size = len(bit_array)

    @classmethod
    def new(cls, expected_elements: int = 100, false_positive_rate: float = 1):
        """
        Create a BloomFilter.
        :param expected_elements: Number of elements expected to be inserted into the BF.
        :param false_positive_rate: Desired false positive rate, as a percent. Lower false positive rate means worse
        performance at the expense of better accuracy.
        """

        # Dynamically adjust the number of hash functions and bit array size based on expected number of elements
        # and the desired false positive rate. Not necessary for a basic Bloom Filter, but this can help to tune
        # performance. Algorithms sourced from Wikipedia page.
        bit_array_size = int(-(expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2))
        num_hash_funcs = int((math.log(2) * (bit_array_size / expected_elements)))

        # This could be improved for memory-efficiency by using a `bitarray`, but that requires installation via pip.
        # initialize bit array to all 0's
        bits = [0] * bit_array_size

        return cls(
            num_hash_funcs=num_hash_funcs,
            bit_array=bits
        )

    @classmethod
    def new_from_file(cls, num_hash_funcs: int, bit_array: [int]):
        """
        Construct a new Bloom Filter from reading a file
        :param num_hash_funcs: Number of hash functions to use
        :param bit_array: List of bits representing the Bloom Filter to use
        """

        return cls(
            num_hash_funcs=num_hash_funcs,
            bit_array=bit_array
        )

    def insert(self, element: str):
        """
        Insert an element into the BF.
        :param element: Element to insert.
        :return: None.
        """

        # iterate over number of hash functions required
        for hf in range(self.num_hash_funcs):
            element_hash = self._hash(element, differentiator=hf)
            position = self._determine_position(element_hash)

            self.bit_array[position] = 1

    def query(self, element: str) -> bool:
        """
        Query the BF for an element. Absence of an element is guaranteed, while presence of an element is only likely.
        :param element: Element to query for.
        :return: False if absent, True if likely present.
        """

        for hf in range(self.num_hash_funcs):
            element_hash = self._hash(element, differentiator=hf)
            position = self._determine_position(element_hash)

            # If any of the bits are a 0, the element is DEFINITELY not in the set
            if self.bit_array[position] == 0:
                return False

        return True

    def get_filter(self) -> [int]:
        """
        Returns the Bloom Filter bit array
        :return: Bloom filter bit array
        """
        return self.bit_array

    def _determine_position(self, hash_: str) -> int:
        # convert hash from hexadecimal to decimal, then modulo with bit array size to ensure the resulting position
        # fits within the bit array
        return int(hash_, 16) % self.bit_array_size

    @staticmethod
    def _hash(element: str, differentiator: int) -> str:
        # hash functions need to return different results, so concatenate the hash function number to the element
        el = f"{element}{differentiator}"

        # generate hash of the element
        return md5(el.encode()).hexdigest()
