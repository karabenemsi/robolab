#!/usr/bin/env python3

import unittest
from hamming_code import HammingCode, HCResult

valid_words = [
    ((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    ((0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1)),
    ((0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0)),
    ((0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1)),
    ((0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1)),
    ((0, 0, 0, 1, 0, 1), (0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0)),
    ((0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1)),
    ((0, 0, 0, 1, 1, 1), (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0)),
    ((0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0)),
    ((0, 0, 1, 0, 0, 1), (0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1)),
    ((0, 0, 1, 0, 1, 0), (0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0)),
    ((0, 0, 1, 0, 1, 1), (0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1)),
    ((0, 0, 1, 1, 0, 0), (0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1)),
    ((0, 0, 1, 1, 0, 1), (0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0)),
    ((0, 0, 1, 1, 1, 0), (0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1)),
    ((0, 0, 1, 1, 1, 1), (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0)),
    ((0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1)),
    ((0, 1, 0, 0, 0, 1), (0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0)),
    ((0, 1, 0, 0, 1, 0), (0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1)),
    ((0, 1, 0, 0, 1, 1), (0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0)),
    ((0, 1, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0)),
    ((0, 1, 0, 1, 0, 1), (0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1)),
    ((0, 1, 0, 1, 1, 0), (0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0)),
    ((0, 1, 0, 1, 1, 1), (0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1)),
    ((0, 1, 1, 0, 0, 0), (0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1)),
    ((0, 1, 1, 0, 0, 1), (0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0)),
    ((0, 1, 1, 0, 1, 0), (0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1)),
    ((0, 1, 1, 0, 1, 1), (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)),
    ((0, 1, 1, 1, 0, 0), (0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0)),
    ((0, 1, 1, 1, 0, 1), (0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1)),
    ((0, 1, 1, 1, 1, 0), (0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0)),
    ((0, 1, 1, 1, 1, 1), (0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1)),
    ((1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1)),
    ((1, 0, 0, 0, 0, 1), (1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0)),
    ((1, 0, 0, 0, 1, 0), (1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1)),
    ((1, 0, 0, 0, 1, 1), (1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0)),
    ((1, 0, 0, 1, 0, 0), (1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)),
    ((1, 0, 0, 1, 0, 1), (1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1)),
    ((1, 0, 0, 1, 1, 0), (1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0)),
    ((1, 0, 0, 1, 1, 1), (1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1)),
    ((1, 0, 1, 0, 0, 0), (1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1)),
    ((1, 0, 1, 0, 0, 1), (1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0)),
    ((1, 0, 1, 0, 1, 0), (1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1)),
    ((1, 0, 1, 0, 1, 1), (1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0)),
    ((1, 0, 1, 1, 0, 0), (1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0)),
    ((1, 0, 1, 1, 0, 1), (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)),
    ((1, 0, 1, 1, 1, 0), (1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0)),
    ((1, 0, 1, 1, 1, 1), (1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1)),
    ((1, 1, 0, 0, 0, 0), (1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0)),
    ((1, 1, 0, 0, 0, 1), (1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1)),
    ((1, 1, 0, 0, 1, 0), (1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0)),
    ((1, 1, 0, 0, 1, 1), (1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1)),
    ((1, 1, 0, 1, 0, 0), (1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1)),
    ((1, 1, 0, 1, 0, 1), (1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0)),
    ((1, 1, 0, 1, 1, 0), (1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1)),
    ((1, 1, 0, 1, 1, 1), (1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0)),
    ((1, 1, 1, 0, 0, 0), (1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0)),
    ((1, 1, 1, 0, 0, 1), (1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1)),
    ((1, 1, 1, 0, 1, 0), (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0)),
    ((1, 1, 1, 0, 1, 1), (1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1)),
    ((1, 1, 1, 1, 0, 0), (1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1)),
    ((1, 1, 1, 1, 0, 1), (1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0)),
    ((1, 1, 1, 1, 1, 0), (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)),
    ((1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0)),
]


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
        test_cases = [
            (
                # From task 4
                (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
                ((1, 0, 1, 1, 0, 1), HCResult.VALID),
            ),
        ]

        for word, encoded_word in valid_words:
            test_cases.append((encoded_word, (word, HCResult.VALID)))

        for code, expected in test_cases:
            self.assertEqual(self.instance.decode(code), expected)

    def test_decode_corrected(self):
        """Essential: Test method decode() with CORRECTED input"""

        test_cases = [
            (
                # From task 4
                (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0),
                ((0, 1, 1, 0, 1, 1), HCResult.CORRECTED),
            ),
            (
                # From task 4
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
                ((0, 0, 0, 0, 0, 0), HCResult.CORRECTED),
            ),
            (
                # From task 4
                (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1),
                ((1, 1, 1, 1, 1, 0), HCResult.CORRECTED),
            ),
        ]

        # Generate all possible single bit errors for valid words
        for word, encoded_word in valid_words:
            for i in range(len(encoded_word)):
                test_cases.append(
                    (
                        tuple(
                            bit ^ (1 if i == j else 0)
                            for j, bit in enumerate(encoded_word)
                        ),
                        (word, HCResult.CORRECTED),
                    )
                )

        for code, expected in test_cases:
            self.assertEqual(self.instance.decode(code), expected)

    def test_decode_uncorrectable(self):
        """Essential: Test method decode() with UNCORRECTABLE input"""
        test_cases = []

        # Generate all possible double bit errors for valid words
        for _, encoded_word in valid_words:
            for i in range(len(encoded_word)):
                for j in range(len(encoded_word)):
                    if i != j:
                        test_cases.append(
                            (
                                tuple(
                                    bit ^ (1 if i == k or j == k else 0)
                                    for k, bit in enumerate(encoded_word)
                                ),
                                (None, HCResult.UNCORRECTABLE),
                            )
                        )

        for code, expected in test_cases:
            self.assertEqual(self.instance.decode(code), expected)

    pass

    def test_encode(self):
        """Essential: Test method encode()"""
        # From task 4
        test_cases = [
            ((0, 1, 1, 0, 1, 1), (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)),
            ((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            ((1, 0, 1, 1, 0, 1), (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)),
            ((1, 1, 1, 1, 1, 0), (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)),
        ]

        # Add all valid words
        for word, encoded_word in valid_words:
            test_cases.append((word, encoded_word))

        for source_word, expected_encoded_word in test_cases:
            self.assertEqual(self.instance.encode(source_word), expected_encoded_word)


if __name__ == "__main__":
    unittest.main()
