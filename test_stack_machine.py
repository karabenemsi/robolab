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

    def test_parse_byte(self):
        pass
if __name__ == "__main__":
    unittest.main()
