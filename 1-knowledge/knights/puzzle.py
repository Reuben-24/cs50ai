from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Helper functions to express the fundamental constraints of the problem.
def character_exists(knight, knave):
    return And(
        # Each character is either a knight or a knave
        Or(knight, knave),
        # A character can not be both a knight and a knave
        Not(And(knight, knave)),
    )


def character_says(knight, knave, *sentences):
    constraints = [character_exists(knight, knave)]
    for sentence in sentences:
        constraints.append(Implication(knight, sentence))
        constraints.append(Implication(knave, Not(sentence)))
    return And(*constraints)


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = character_says(AKnight, AKnave, And(AKnight, AKnave))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    character_says(AKnight, AKnave, And(AKnave, BKnave)),
    character_exists(BKnight, BKnave),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASentence = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BSentence = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    character_says(AKnight, AKnave, ASentence),
    character_says(BKnight, BKnave, BSentence),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASentence = Or(AKnight, AKnave)
BSentence1 = Implication(ASentence, AKnave)
BSentence2 = CKnave
CSentence = AKnight

knowledge3 = And(
    character_says(AKnight, AKnave, ASentence),
    character_says(BKnight, BKnave, BSentence1, BSentence2),
    character_says(CKnight, CKnave, CSentence)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
