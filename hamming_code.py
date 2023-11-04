#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


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
        return sum(
            2**i * bit
            for i, bit in enumerate(
                sum(a * b for a, b in zip(x, col)) % 2 for col in self.h
            )
        )

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
        overall_parity_bit = encoded_word[-1]
        overall_parity_ok = sum(encoded_word) % 2 == overall_parity_bit
        syndrome = self.__get_syndrome(encoded_word[:-1])

        if overall_parity_ok and syndrome == 0:
            # No error
            return tuple(encoded_word[: self.data_bits]), HCResult.VALID
        elif not overall_parity_ok and syndrome == 0:
            # Error in overall parity bit, data is valid
            return tuple(encoded_word[: self.data_bits]), HCResult.VALID
        elif overall_parity_ok and syndrome >= 1:
            # Multiple errors, uncorrectable
            return None, HCResult.UNCORRECTABLE
        elif not overall_parity_ok and syndrome >= 1:
            # while sum(syndrome) >= 1:
            # TODO: Implement error correction
            return tuple(encoded_word[: self.data_bits]), HCResult.CORRECTED
            # while syndrome_number >= 1 and overall_parity == 1:
            #     print("Error on position " + str(syndrome_number) + ". Try to correct it")
            #     corrected_vector = tuple(
            #         bit ^ (1 if i == syndrome_number - 1 else 0)
            #         for i, bit in enumerate(vector)
            #     )
            #     print(f"Corrected vector: {corrected_vector}")
            #     print(f"Corrected check: {get_syndrome(corrected_vector, H_sys)}")
            #     *syndrome, overall_parity = get_syndrome(corrected_vector, H_sys)
            #     syndrome_number = sum(2**i * bit for i, bit in enumerate(syndrome))
            #     if syndrome_number == 0 and overall_parity == 0:
            #         print("Corrected!")
            #         break
            #     elif syndrome_number >= 1 and overall_parity == 0:
            #         print("Multiple errors")
            #         break
