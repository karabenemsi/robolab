# %%
from typing import Tuple, Dict

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
    (1, 1, 1, 0, 0, 0, 0, 1),
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
    print(
        f"{word}: {encoded}, Parity: {encoded[-1]} -> {sum(encoded) % 2 == 0}"
    )

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
    print(
        f"Word {word}: Syndrome: {syndrome} ({syndrome_number}), overall_parity: {overall_parity}"
    )
    if syndrome_number == 0 and overall_parity == 0:
        print("\tno error")
    elif syndrome_number == 0 and overall_parity == 1:
        print("\tError in p4")
    elif syndrome_number >= 1 and overall_parity == 1:
        while syndrome_number >= 1 and overall_parity == 1:
            print("\tError on position " + str(syndrome_number) + ". Try to correct it")
            vector = tuple(
                bit ^ (1 if i == syndrome_number - 1 else 0)
                for i, bit in enumerate(vector)
            )
            print(f"\tCorrected vector: {vector}")
            print(f"\tCorrected check: {get_syndrome(vector, H_sys)}")
            *syndrome, overall_parity = get_syndrome(vector, H_sys)
            syndrome_number = sum(2**i * bit for i, bit in enumerate(syndrome))
            if(syndrome_number == 0 and overall_parity == 0):
                print("\tCorrected!")
                break
            elif(syndrome_number >= 1 and overall_parity == 0):
                print("\tMultiple errors")
                break
    else:
        print("\tMultiple errors")
    print()
