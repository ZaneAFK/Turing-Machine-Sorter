"""
The machine is a bubble sort on adjacent words, using only the head position and the state.
Two neighbouring words A and B have their matching digits exactly 17 cells apart, so the
machine compares them digit by digit by carrying one digit across that distance inside its
state. When A > B it swaps the words digit by digit, from the first differing digit onwards.
A pass that swaps anything sets a flag (kept in the state, 0 or 1), and the machine repeats
passes until one completes with no swap.

State names (flag is 0 = nothing swapped yet this pass, 1 = something swapped):
    P{flag}            at the first digit of word A, ready to compare it with B
    C{flag}_{x}_{k}    carrying digit x of A right, k cells so far
    D{flag}_{x}        at digit i of B, comparing it with the carried digit x
    E{flag}_{k}        digits equal: walking back to A, k cells so far
    Q{flag}, N{flag}   back at digit i of A, stepping on to digit i + 1
    S{flag}            A < B: scanning left to the comma before B
    L_{e}_{k}          carrying B's digit e left to A, k cells so far
    W_{e}              at digit i of A, writing the carried digit e
    X                  after the swapped digit: picking up the next digit of A
    R_{y}_{k}          carrying digit y of A right to B, k cells so far
    V_{y}              at digit i of B, writing A's digit y and picking up B's old digit
    B{flag}            end of the list: rewinding to the opening bracket
"""
import argparse

DIGITS = '0123456789ABCDEF'
WORD_LENGTH = 16
WALKABLE = DIGITS + ','  # symbols a walking state passes over

START_STATE = '⎆'
ACCEPT_STATE = '✔'
RIGHT, LEFT, HALT = '→', '←', '⏹'
KEEP = ''  # an empty "next symbol" leaves the cell unchanged


class Table:
    """The rows of the machine file."""

    def __init__(self):
        self.rows = []

    def Add(self, state, symbols, move, write, nextState):
        """One row: in `state`, on any of `symbols`, write `write`, move, and go to `nextState`."""
        self.rows.append('\t'.join((state, ' '.join(symbols), move, write, nextState)))

    def AddWalk(self, name, symbols, move, nextState):
        """A chain of states name_1 .. name_16 that moves over WORD_LENGTH cells, then goes to `nextState`."""
        for k in range(1, WORD_LENGTH):
            self.Add(f'{name}_{k}', symbols, move, KEEP, f'{name}_{k + 1}')
        self.Add(f'{name}_{WORD_LENGTH}', symbols, move, KEEP, nextState)

    def Text(self):
        return '\n'.join(self.rows) + '\n'


def AddStartAndFinish(table):
    table.Add(START_STATE, '[', RIGHT, KEEP, 'P0')
    table.Add('P0', ']', LEFT, KEEP, 'B0')          # empty list: nothing to sort
    table.Add('B1', '[', RIGHT, KEEP, 'P0')         # something was swapped: start a new pass
    table.Add('B0', '[', HALT, KEEP, ACCEPT_STATE)  # a pass with no swap: sorted, head at cell 0


def AddRewind(table, flag):
    """At the end of the list, scan left to the opening bracket."""
    table.Add(f'B{flag}', WALKABLE + ']', LEFT, KEEP, f'B{flag}')


def AddCompare(table, flag):
    """Compare digit i of A with digit i of B, for each i, until they differ or A ends."""
    for digit in DIGITS:
        # Pick up digit i of A and carry it right to digit i of B.
        table.Add(f'P{flag}', digit, RIGHT, KEEP, f'C{flag}_{digit}_1')
        table.AddWalk(f'C{flag}_{digit}', WALKABLE, RIGHT, f'D{flag}_{digit}')
        # A was the last word, so there is no B: pass over it.
        table.Add(f'C{flag}_{digit}_{WORD_LENGTH}', ']', LEFT, KEEP, f'B{flag}')

        for other in DIGITS:
            if other < digit:    # A > B: write A's digit into B and go and swap
                table.Add(f'D{flag}_{digit}', other, LEFT, digit, f'L_{other}_1')
            elif other > digit:  # A < B: no swap
                table.Add(f'D{flag}_{digit}', other, LEFT, KEEP, f'S{flag}')
        table.Add(f'D{flag}_{digit}', digit, LEFT, KEEP, f'E{flag}_1')  # equal: go back to A

        # Step on to digit i + 1 of A, or, if A has ended, the words were equal.
        table.Add(f'N{flag}', digit, RIGHT, KEEP, f'C{flag}_{digit}_1')

    table.AddWalk(f'E{flag}', WALKABLE, LEFT, f'Q{flag}')
    table.Add(f'Q{flag}', DIGITS, RIGHT, KEEP, f'N{flag}')
    table.Add(f'N{flag}', ',', RIGHT, KEEP, f'P{flag}')  # equal words: next pair starts at B

    table.Add(f'S{flag}', DIGITS, LEFT, KEEP, f'S{flag}')  # scan left to the comma before B
    table.Add(f'S{flag}', ',', RIGHT, KEEP, f'P{flag}')    # next pair starts at B


def AddSwap(table):
    """A > B: swap the words digit by digit, starting at the first differing digit."""
    for digit in DIGITS:
        # Carry B's digit left to A, and write it there.
        table.AddWalk(f'L_{digit}', WALKABLE, LEFT, f'W_{digit}')
        table.Add(f'W_{digit}', DIGITS, RIGHT, digit, 'X')

        # Pick up the next digit of A and carry it right to B, writing it there and
        # picking up B's old digit to carry back.
        table.Add('X', digit, RIGHT, KEEP, f'R_{digit}_1')
        table.AddWalk(f'R_{digit}', WALKABLE, RIGHT, f'V_{digit}')
        for other in DIGITS:
            table.Add(f'V_{digit}', other, LEFT, digit, f'L_{other}_1')

    table.Add('X', ',', RIGHT, KEEP, 'P1')  # A fully swapped: set the flag, next pair


def GenerateTSV():
    """Return the sorter's machine file as TSV text."""
    table = Table()
    AddStartAndFinish(table)
    for flag in '01':
        AddRewind(table, flag)
        AddCompare(table, flag)
    AddSwap(table)
    return table.Text()


def GenerateAndWriteTSV(path):
    with open(path, 'w', encoding='utf-8', newline='\n') as file:
        file.write(GenerateTSV())


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-o', '--output', required=True, help='file to write the machine to')
    arguments = argParser.parse_args()
    GenerateAndWriteTSV(arguments.output)


if __name__ == '__main__':
    main()
