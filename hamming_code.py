#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union
from functools import reduce


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE
Matrix = List[List[int]]


class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """

    VALID = "OK"
    CORRECTED = "FIXED"
    UNCORRECTABLE = "ERROR"


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        gns: Matrix = [
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        ]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __transpose(self, matrix: Matrix) -> Matrix:
        """
        Transposes the given matrix.

        Args:
            matrix (list): Matrix to transpose
        Returns:
            list: Transposed matrix
        """

        return list(map(list, zip(*matrix)))

    def __convert_to_g(self, gns: Matrix) -> Matrix:
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        g = gns.copy()
        steps = [
            (1, (3, 5, 6)),
            (2, (1, 3, 6)),
            (3, (1, 5, 6)),
            (4, (1, 3)),
            (5, (2, 3)),
            (6, (1, 2, 5)),
        ]
        for step in steps:
            working_row = g[step[0] - 1]
            for target_row in step[1]:
                g[target_row - 1] = [
                    (a - b) % 2 for a, b in zip(working_row, g[target_row - 1])
                ]
        return g

    def __derive_h(self, g: Matrix) -> Matrix:
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """
        identity_matrix = [
            [1 if i == j else 0 for i in range(self.parity_bits)]
            for j in range(self.parity_bits)
        ]
        parity_matrix = self.__transpose(g)[self.data_bits :]
        return [a + b for a, b in zip(parity_matrix, identity_matrix)]

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """
        encoded_word = tuple(
            sum(a * b for a, b in zip(source_word, col)) % 2
            for col in self.__transpose(self.g)
        )

        return encoded_word + (sum(encoded_word) % 2,)

    def __get_syndrome(self, x: Tuple[int, ...]) -> int:
        """
        Returns the syndrome of the given word.

        Args:
            x (tuple): n-tuple (length depends on number of total bits)
        Returns:
            tuple: r-tuple (length depends on number of parity bits)
        """
        return tuple(sum(a * b for a, b in zip(x, col)) % 2 for col in self.h)

    def decode(
        self, encoded_word: Tuple[int, ...]
    ) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """
        overall_parity_ok = sum(encoded_word) % 2 == 0
        syndrome = self.__get_syndrome(encoded_word[:-1])
        syndrome_bits = sum(syndrome)



        if overall_parity_ok and syndrome_bits == 0:
            # No error
            return tuple(encoded_word[: self.data_bits]), HCResult.VALID
        elif not overall_parity_ok and syndrome_bits == 0:
            # Error in overall parity bit, data is valid
            return tuple(encoded_word[: self.data_bits]), HCResult.CORRECTED
        
        elif overall_parity_ok and syndrome_bits >= 1:
            # Multiple errors, uncorrectable
            return None, HCResult.UNCORRECTABLE
        elif not overall_parity_ok and syndrome_bits >= 1:
            encoded_word = list(encoded_word)
            # Search for the column in H that matches the syndrome
            error_position_mask = reduce(
                # and all the columns, resulting in a tuple of 1s and 0s where 1s indicate the error positions
                lambda total, new: tuple(a & b  for a,b in zip(total , new)),
                # for each row in H, return the row if the syndrome bit is 1, otherwise return the row with all bits flipped
                # when anding the rows, the result will be a tuple of 1s and 0s where 1s indicate the positions the syndrome matches the column
                (mask if s == 1 else tuple(val^1 for val in mask) for s, mask in zip(syndrome, self.h))
            )
            # get the positions of the 1s in the mask
            error_positions = tuple(i for i, v in enumerate(error_position_mask) if v == 1)
            # if there are no error positions or more than 1, the error is uncorrectable
            if(len(error_positions) != 1):
                return None, HCResult.UNCORRECTABLE
            # if there is exactly one error position, flip the bit at that position
            encoded_word = tuple(
                bit ^ (1 if i == error_positions[0] else 0)
                for i, bit in enumerate(encoded_word)
            )
            return encoded_word[:self.data_bits], HCResult.CORRECTED
        else:
            raise Exception("This should never happen")
