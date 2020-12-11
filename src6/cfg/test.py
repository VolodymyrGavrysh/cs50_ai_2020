import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP V

    NP -> N | A NP

    A -> "small" | "white"
    N -> "cats" | "trees"
    V -> "climb" | "run"
""")

parser = nltk.ChartParser(grammar)

sentence = input("Sentence: ").split()
try:
    for tree in parser.parse(sentence):
        tree.pretty_print()
        tree.draw()
except ValueError:
    print("No parse tree possible.")
