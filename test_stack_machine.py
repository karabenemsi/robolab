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
        # Test when byte is a number
        for i in range(0, 15):
            self.assertEqual(
                self.sm._parse_byte(tuple(int(bit) for bit in bin(i)[2:].zfill(6))), i
            )

        # Test when byte is an instruction
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.STP.value)),
            Instruction.STP,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.DUP.value)),
            Instruction.DUP,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.DEL.value)),
            Instruction.DEL,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.SWP.value)),
            Instruction.SWP,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.ADD.value)),
            Instruction.ADD,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.SUB.value)),
            Instruction.SUB,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.MUL.value)),
            Instruction.MUL,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.DIV.value)),
            Instruction.DIV,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.EXP.value)),
            Instruction.EXP,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.MOD.value)),
            Instruction.MOD,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.SHL.value)),
            Instruction.SHL,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.SHR.value)),
            Instruction.SHR,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.HEX.value)),
            Instruction.HEX,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.FAC.value)),
            Instruction.FAC,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.NOT.value)),
            Instruction.NOT,
        )
        self.assertEqual(
            self.sm._parse_byte(self._inputValueToTuple(Instruction.XOR.value)),
            Instruction.XOR,
        )

        # Test when byte is a special case
        self.assertEqual(self.sm._parse_byte((1, 0, 0, 0, 0, 0)), Instruction.NOP)
        self.assertEqual(self.sm._parse_byte((1, 0, 0, 0, 0, 1)), Instruction.SPEAK)
        self.assertEqual(self.sm._parse_byte((1, 0, 0, 0, 1, 0)), " ")
        self.assertEqual(self.sm._parse_byte((1, 0, 0, 0, 1, 1)), Instruction.NOP)
        self.assertEqual(self.sm._parse_byte((1, 1, 1, 1, 1, 0)), Instruction.NOP)
        self.assertEqual(self.sm._parse_byte((1, 1, 1, 1, 1, 1)), Instruction.NOP)

        # Test when byte is a letter
        for i in range(0, 26):
            self.assertEqual(
                self.sm._parse_byte(
                    tuple(int(bit) for bit in bin(i + 36)[2:].zfill(6))
                ),
                chr(ord("A") + i),
            )

    def test_pop_operands_from_stack(self):
        init_stack = [
            self._intToByteTuple(1),
            (0, 0, 0, 0, 0, 0, 1, 1),
            (0, 0, 0, 0, 0, 1, 1, 1),
            (0, 0, 0, 0, 1, 1, 1, 1),
            (0, 0, 0, 1, 1, 1, 1, 1),
        ]
        self.sm.stack = init_stack.copy()
        self.assertEqual(self.sm._pop_operands_from_stack(1), (31,))
        self.assertEqual(self.sm.stack, init_stack[:-1])

        self.sm.stack = init_stack.copy()
        self.assertEqual(self.sm._pop_operands_from_stack(2), (31, 15))
        self.assertEqual(self.sm.stack, init_stack[:-2])

        self.sm.stack = init_stack.copy()
        self.assertEqual(self.sm._pop_operands_from_stack(3), (31, 15, 7))
        self.assertEqual(self.sm.stack, init_stack[:-3])

        self.sm.stack = []
        self.sm._push(15)
        self.sm._push(14)
        self.sm._push(13)
        self.assertEqual(self.sm._pop_operands_from_stack(3), (13, 14, 15))

        # Test when stack is empty
        self.sm.stack = []
        with self.assertRaises(IndexError):
            self.sm._pop_operands_from_stack(1)

        # Test when stack has less elements than requested
        self.sm.stack = [self._intToByteTuple(1)]
        with self.assertRaises(IndexError):
            self.sm._pop_operands_from_stack(2)

        # Test with characters
        self.sm.stack = []
        self.sm._push("A")
        self.sm._push("B")
        self.sm._push("C")
        self.assertEqual(self.sm._pop_operands_from_stack(3), ("C", "B", "A"))
if __name__ == "__main__":
    unittest.main()
