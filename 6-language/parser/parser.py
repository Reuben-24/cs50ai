import nltk
from nltk.tokenize import word_tokenize
import sys
import string

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S | S Conj VP
VP -> V | V NP | NP V | V PP | Adv V NP | V Adv | V NP PP | V Adv PP
NP -> N | Det N | Det N PP | Det Adj N | Det Adj Adj Adj N
PP -> P NP | P NP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = word_tokenize(sentence)

    cleaned_tokens = [
        token.lower() for token in tokens if any(char.isalpha() for char in token)
    ]

    return cleaned_tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for subtree in tree.subtrees():
        # Only consider NP subtrees
        if subtree.label() == "NP":
            # Assume initially it is a chunk
            is_chunk = True

            # Check all descendants to see if there is another NP inside
            for descendant in subtree.subtrees():
                if descendant == subtree:
                    continue  # Skip the parent tree
                if descendant.label() == "NP":
                    is_chunk = False
                    break

            if is_chunk:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()
