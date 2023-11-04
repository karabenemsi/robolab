#!/usr/bin/env python3

import unittest
from hamming_code import HammingCode, HCResult


class TestHammingCode(unittest.TestCase):
    # Init test class with HammingCode instance for all test methods
    def __init__(self, *args, **kwargs) -> None:
        self.instance = HammingCode()
        super().__init__(*args, **kwargs)

    def test_instance(self):
        """ Essential: Test class instantiation """
        self.fail('implement me!')

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        self.fail('implement me!')

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        self.fail('implement me!')

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        self.fail('implement me!')

    def test_encode(self):
        """ Essential: Test method encode() """
        self.fail('implement me!')


if __name__ == '__main__':
    unittest.main()
