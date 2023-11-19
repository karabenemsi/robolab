from enum import Enum


class Associativity(Enum):
    LEFT = 1
    RIGHT = 2


operators: dict[str, dict[str, Associativity]] = {
    "*": {"precedence": 3, "associativity": Associativity.LEFT},
    "/": {"precedence": 3, "associativity": Associativity.LEFT},
    "+": {"precedence": 2, "associativity": Associativity.LEFT},
    "-": {"precedence": 2, "associativity": Associativity.LEFT},
}


def shunting_yard(input: str) -> str:
    input = input.replace(" ", "")
    operations = operators.keys()
    stack = []
    output = []
    for token in input:
        if token.isnumeric():
            output.append(token)
        elif token in operations:
            op1 = operators[token]
            while (
                len(stack) > 0
                and stack[-1] in operations
                and (
                    operators[stack[-1]]["precedence"] > op1["precedence"]
                    or (
                        operators[stack[-1]]["precedence"] == op1["precedence"]
                        and operators[stack[-1]]["associativity"] == Associativity.LEFT
                    )
                )
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                assert len(stack) > 0
                output.append(stack.pop())
            assert stack[-1] == "("
            stack.pop()
        else:
            raise Exception(f"Unknown token: {token}")
    while len(stack) > 0:
        output.append(stack.pop())
    return " ".join(output)


examples = [
    "4*(7+8*9)-1",
    "(96 - (4 + 44 * (3 - 1) + 7) * 25)",
    "((5*5*5) / ( 2 + 3)) / 5",
]

for example in examples:
    print(shunting_yard(example))

# Prints:
# 4789*+*1-
# 9644431-*+7+25*-
# 55*5*23+/5/