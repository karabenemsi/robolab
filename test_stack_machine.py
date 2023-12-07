#!/usr/bin/env python3

import unittest
from stack_machine import StackMachine, Instruction, SMState


class TestStackMachine(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        self.sm = StackMachine()
        super().__init__(*args, **kwargs)

    def test_instance(self):
        """Essential: Test class instantiation"""
        sm = StackMachine()
        self.assertIsInstance(sm, StackMachine)
        self.assertEqual(sm.overflow, False)
        self.assertEqual(sm.stack, [])

    def test_top(self):
        # Test when stack is empty
        self.assertIsNone(self.sm.top())

        # Test when stack has one element appended
        self.sm.stack.append((0, 1, 0, 1, 0, 1, 0, 1, 0))
        self.assertEqual(self.sm.top(), (0, 1, 0, 1, 0, 1, 0, 1, 0))

        # Test when stack has multiple elements appended
        self.sm.stack.append((0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(self.sm.top(), (0, 0, 0, 0, 0, 0, 0, 0, 0))

        self.sm.stack = [
            self._intToByteTuple(255),
            (1, 1, 1, 1, 1, 1, 1, 0),
            (1, 1, 1, 1, 1, 1, 0, 0),
            (1, 1, 1, 1, 1, 0, 0, 0),
        ]
        self.assertEqual(self.sm.top(), (1, 1, 1, 1, 1, 0, 0, 0))

    def test_push(self):
        # Push an integer
        self.sm.stack = []
        self.sm._push(1)
        self.assertEqual(self.sm.stack, [self._intToByteTuple(1)])

        # Push a tuple
        self.sm.stack = []
        self.sm._push(
            (1, 1, 1, 1, 1, 0, 0, 0),
        )
        self.assertEqual(
            self.sm.stack,
            [
                (1, 1, 1, 1, 1, 0, 0, 0),
            ],
        )

        # Push a character
        self.sm.stack = []
        self.sm._push("A")
        self.assertEqual(self.sm.stack, ["A"])

        # Push multiple tuples and integers
        self.sm.stack = []
        self.sm._push(1)
        self.sm._push(self._intToByteTuple(2))
        self.sm._push("B")
        self.sm._push((1, 1, 1, 1, 1, 0, 0, 0))
        self.sm._push(self._intToByteTuple(255))
        self.assertEqual(
            self.sm.stack,
            [
                self._intToByteTuple(1),
                self._intToByteTuple(2),
                "B",
                (1, 1, 1, 1, 1, 0, 0, 0),
                self._intToByteTuple(255),
            ],
        )

    def _inputValueToTuple(self, value: int) -> tuple:
        return tuple(int(bit) for bit in bin(value)[2:].zfill(6))

    def _intToByteTuple(self, value: int) -> tuple:
        return tuple(int(bit) for bit in bin(value)[2:].zfill(8))

    def _tupleToByteInt(self, value: tuple) -> int:
        return int("".join([str(i) for i in value]), 2)

    def test_parse_byte(self):
        pass
if __name__ == "__main__":
    unittest.main()
