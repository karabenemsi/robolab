#!/usr/bin/env python3

from enum import IntEnum, Enum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE


class Instruction(Enum):
    STP = 0b010000
    DUP = 0b010001
    DEL = 0b010010
    SWP = 0b010011
    ADD = 0b010100
    SUB = 0b010101
    MUL = 0b010110
    DIV = 0b010111
    EXP = 0b011000
    MOD = 0b011001
    SHL = 0b011010
    SHR = 0b011011
    HEX = 0b011100
    FAC = 0b011101
    NOT = 0b011110
    XOR = 0b011111
    NOP = None
    SPEAK = 0b100001

    def __str__(self):
        return self.name


class SMState(IntEnum):
    """
    Return codes for the stack machine
    """

    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack: List[int or str] = []

    def _parse_byte(self, code_word: Tuple[int, ...]) -> int or Instruction or str:
        # TODO: tuple of bin to int
        byte = int("".join([str(i) for i in code_word]), 2)
        if 0 <= byte <= 15:
            # Is a number
            return byte
        elif 16 <= byte <= 31:
            # Is an instruction
            return Instruction(byte)
        elif 32 <= byte <= 35:
            # Is a special case
            if byte == 33:
                return Instruction.SPEAK
            elif byte == 34:
                return " "
            else:
                return Instruction.NOP
        elif 36 <= byte <= 61:
            # Is a letter
            return chr(ord("A") + byte - 36)
        else:
            return Instruction.NOP

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        word = self._parse_byte(code_word)
        if isinstance(word, Instruction):
            try:
                return self._run_instruction(word)
            except IndexError as ie:
                print(f"IndexError: {ie}")
                return SMState.ERROR
            except NotImplementedError:
                return SMState.ERROR
            except ZeroDivisionError:
                return SMState.ERROR
            except ValueError:
                return SMState.ERROR
            except Exception as e:
                print(f"Unknown error: {e}")
                return SMState.ERROR
        else:
            self._push(word)
            self.overflow = False
            return SMState.RUNNING

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """
        return self.stack[-1] if len(self.stack) > 0 else None

    def _push(
        self, value: int or Tuple[int, int, int, int, int, int, int, int] or str
    ) -> None:
        """
        Pushes a value on the stack.
        """
        # Convert to Tuple if int
        if isinstance(value, int):
            self.stack.append(tuple(int(bit) for bit in bin(value)[2:].zfill(8)))
        elif isinstance(value, tuple):
            self.stack.append(value)
        elif isinstance(value, str):
            if len(value) != 1:
                raise ValueError("String must be of length 1")
            self.stack.append(value)

    def _pop_operands_from_stack(self, n=2) -> Tuple[int or str, ...]:
        """
        Pops n operands from the stack. and returns them as a tuple. If the stack has (k-m, ..., k-1, k) elements, where k is the top most element, the order of operands in the tuple is (k, k-1, ..., k-n)

        Raises:
            IndexError: If stack is k < n elements

        Returns:
            tuple: Tuple of n operands
        """
        if len(self.stack) < n:
            raise IndexError("operand mismatch")
        else:
            return tuple(
                int("".join([str(i) for i in self.stack.pop()]), 2)
                if isinstance(self.stack[-1], tuple)
                else self.stack.pop()
                for _ in range(n)
            )

    def _run_instruction(self, instr: Instruction) -> SMState:
        MAX_INT = 255
        if instr == Instruction.STP:
            return SMState.STOPPED
        elif instr == Instruction.DUP:
            ops = self._pop_operands_from_stack(1)
            self._push(ops[0])
            self._push(ops[0])
        elif instr == Instruction.DEL:
            print("Do DEL")
        elif instr == Instruction.SWP:
            print("Do SWP")
        elif instr == Instruction.ADD:
            ops = self._pop_operands_from_stack()
            result = ops[1] + ops[0]
            if result > MAX_INT:
                result %= MAX_INT + 1
                self.overflow = True
            else:
                self.overflow = False
            self._push(result)
        elif instr == Instruction.SUB:
            ops = self._pop_operands_from_stack()
            result = ops[1] - ops[0]
            if result < 0:
                result = (MAX_INT + 1) + result
                self.overflow = True
            else:
                self.overflow = False
            self._push(result)
        elif instr == Instruction.MUL:
            ops = self._pop_operands_from_stack()
            result = ops[1] * ops[0]
            if result > MAX_INT:
                result %= MAX_INT + 1
                self.overflow = True
            else:
                self.overflow = False
            self._push(result)
        elif instr == Instruction.DIV:
            ops = self._pop_operands_from_stack()
            self.overflow = False
            self._push(ops[1] // ops[0])
        elif instr == Instruction.EXP:
            ops = self._pop_operands_from_stack()
            result = ops[1] ** ops[0]

            if result > MAX_INT:
                result %= MAX_INT + 1
                self.overflow = True
            else:
                self.overflow = False
            self._push(result)
        elif instr == Instruction.MOD:
            self.overflow = False
            ops = self._pop_operands_from_stack()
            result = ops[1] % ops[0]
            self._push(result)
        elif instr == Instruction.SHL:
            print("Do SHL")
        elif instr == Instruction.SHR:
            self.overflow = False
            ops = self._pop_operands_from_stack()
            result = ops[1] >> ops[0]
            self._push(result)
        elif instr == Instruction.HEX:
            print("Do HEX")
        elif instr == Instruction.FAC:
            print("Do FAC")
        elif instr == Instruction.NOT:
            print("Do NOT")
        elif instr == Instruction.XOR:
            self.overflow = False
            ops = self._pop_operands_from_stack()
            result = ops[1] ^ ops[0]
            self._push(result)
        elif instr == Instruction.NOP:
            print("Do NOP")
        elif instr == Instruction.SPEAK:
            print("Do SPEAK")
        return 0
