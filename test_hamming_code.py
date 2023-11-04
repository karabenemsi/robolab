#!/usr/bin/env python3

import unittest
from hamming_code import HammingCode, HCResult


class TestHammingCode(unittest.TestCase):
    # Init test class with HammingCode instance for all test methods
    def __init__(self, *args, **kwargs) -> None:
        self.instance = HammingCode()
        super().__init__(*args, **kwargs)

    def test_instance(self):
        """Essential: Test class instantiation"""
        self.assertIsInstance(self.instance, HammingCode)
        self.assertEqual(self.instance.total_bits, 10)
        self.assertEqual(self.instance.data_bits, 6)
        self.assertEqual(self.instance.parity_bits, 4)
        self.assertEqual(
            self.instance.g,
            [
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            ],
        )
        self.assertEqual(
            self.instance.h,
            [
                [1, 0, 1, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
            ],
        )

    def test_transpose(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.assertEqual(self.instance._HammingCode__transpose(matrix), expected)

    def test_decode_valid(self):
        """Essential: Test method decode() with VALID input"""
        codes_to_decode = [
            (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0),
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),  # From task 4
            (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1),
        ]
        expected_results = [
            ((0, 1, 1, 0, 1, 1), HCResult.VALID),
            ((0, 0, 0, 0, 0, 0), HCResult.VALID),
            ((1, 0, 1, 1, 0, 1), HCResult.VALID),
            ((1, 1, 1, 1, 1, 0), HCResult.VALID),
        ]
        for code, expected in zip(codes_to_decode, expected_results):
            self.assertEqual(self.instance.decode(code), expected)

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        self.fail('implement me!')

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        self.fail('implement me!')

    def test_encode(self):
        """Essential: Test method encode()"""
        test_cases = [
            ((0, 1, 1, 0, 1, 1), (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)),
            ((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            ((1, 0, 1, 1, 0, 1), (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)),
            ((1, 1, 1, 1, 1, 0), (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)),
        ]

        for source_word, expected_encoded_word in test_cases:
            self.assertEqual(self.instance.encode(source_word), expected_encoded_word)


if __name__ == "__main__":
    unittest.main()
