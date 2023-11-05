# %%
from typing import Tuple, Dict
from functools import reduce

Matrix = Tuple[Tuple[int, ...], ...]


def transpose(matrix: Matrix) -> Matrix:
    """Return the transpose of a matrix."""
    return tuple(zip(*matrix))


# %%
G_non_sys: Matrix = (
    (1, 1, 1, 0, 0, 0, 0, 1),
    (1, 0, 0, 1, 1, 0, 0, 1),
    (0, 1, 0, 1, 0, 1, 0, 1),
    (1, 1, 0, 1, 0, 0, 1, 0),
)
H_non_sys: Matrix = (
    (1, 0, 1, 0, 1, 0, 1, 0),
    (0, 1, 1, 0, 0, 1, 1, 0),
    (0, 0, 0, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1),
)
G_sys: Matrix = (
    (1, 0, 0, 0, 0, 1, 1, 1),
    (0, 1, 0, 0, 1, 0, 1, 1),
    (0, 0, 1, 0, 1, 1, 0, 1),
    (0, 0, 0, 1, 1, 1, 1, 0),
)
H_sys: Matrix = (
    (0, 1, 1, 1, 1, 0, 0, 0),
    (1, 0, 1, 1, 0, 1, 0, 0),
    (1, 1, 0, 1, 0, 0, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1),
)

# %%
Vector = Tuple[int, ...]


def encode(a: Vector, G: Matrix) -> Vector:
    """Encode a message vector using a generator matrix."""
    return tuple(sum(a * b for a, b in zip(a, col)) % 2 for col in transpose(G))


# %%
words: Dict[str, Vector] = {
    "1": (0, 1, 0, 0),
    "2": (1, 0, 0, 1),
    "3": (0, 0, 1, 1),
    "4": (1, 1, 0, 1),
}

print("Task 3, encode with non-systematic matrix")
for word, vector in words.items():
    encoded = encode(vector, G_non_sys)
    print(f"{word}: {encoded}, Parity: {encoded[-1]} -> {'correct' if sum(encoded) % 2 == 0 else 'incorrect'}")

# %%


# %%
words_2: Dict[str, Vector] = {
    "1": (1, 1, 0, 0, 1, 1, 0, 1),
    "2": (1, 0, 0, 1, 1, 0, 0, 1),
    "3": (1, 1, 0, 1, 1, 0, 1, 1),
    "4": (1, 1, 0, 1, 0, 1, 0, 1),
}


# %%
def get_syndrome(x: Vector, H: Matrix) -> Vector:
    """Check if a vector has the correct parity."""
    return tuple(sum(a * b for a, b in zip(x, col)) % 2 for col in H)


print("Task 4, check with non-systematic matrix")
for word, vector in words_2.items():
    *syndrome, overall_parity = get_syndrome(vector, H_sys)
    syndrome_number = sum(2**i * bit for i, bit in enumerate(syndrome))
    syndrome_bits = sum(syndrome)

    print(
        f"Word {word}: Syndrome with parity: {syndrome + [overall_parity]} ({syndrome_bits}), overall_parity: (p4:{vector[-1]}) -> {'correct' if overall_parity == 0 else 'incorrect'}"
    )
    if syndrome_bits == 0 and overall_parity == 0:
        print("\tno error")
    elif syndrome_bits == 0 and overall_parity == 1:
        print("\tError in p4")
    elif syndrome_bits >= 1 and overall_parity == 1:
        print("\terror, try to correct it")
        vector = list(vector)
        # Search for the column in H that matches the syndrome
        error_position_mask = reduce(
            # and all the columns, resulting in a tuple of 1s and 0s where 1s indicate the error positions
            lambda total, new: tuple(a & b for a, b in zip(total, new)),
            # for each row in H, return the row if the syndrome bit is 1, otherwise return the row with all bits flipped
            # when anding the rows, the result will be a tuple of 1s and 0s where 1s indicate the positions the syndrome matches the column
            (
                mask if s == 1 else tuple(val ^ 1 for val in mask)
                for s, mask in zip(syndrome + [overall_parity], H_sys)
            ),
        )
        # get the positions of the 1s in the mask
        error_positions = tuple(i for i, v in enumerate(error_position_mask) if v == 1)
        # if there are no error positions or more than 1, the error is uncorrectable
        if len(error_positions) == 0:
            print("\tsyndrome does not match any column in H, multiple errors")
        elif len(error_positions) != 1:
            print("\tsyndrome matches multiple columns in H, multiple errors")
        # if there is exactly one error position, flip the bit at that position
        else:
            print(f"\t error position: {error_positions[0]}")
            vector[error_positions[0]] = vector[error_positions[0]] ^ 1
            print(f"\tcorrected vector: {vector}")
            print(f"\tcorrected syndrome: {get_syndrome(vector, H_sys)}")
    else:
        print("\tMultiple errors")
    print()
