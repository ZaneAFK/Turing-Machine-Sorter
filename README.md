# Turing-Machine-Sorter

A toolchain for building and testing a Turing machine that sorts a list of 16-digit hex words.

The sorter is written in the 40908 Theory of Computing Science course's Turing Machine Specification Format, a five-column tab-separated (TSV) file. The TSV file is the turing machine which is produced by `Generator.py`.

## Repository structure

```
.
├── README.md
└── src/
    ├── Machine.py          the Turing machine and its run loop
    ├── Parser.py           reads a machine file into a machine, and lints it
    ├── Simulator.py        runs a machine file on an input
    ├── Generator.py        writes the sorter's machine file
    └── test/
        ├── ParserTest.py   tests for the parser
        └── MachineTest.py  tests for the machine and the generated sorter
```

- **Machine** holds the rule table and runs it on an input. A run ends with a result made of the final state, the tape contents and the head position. The final state is the accept state on success, the error state on a missing transition or a move off the left edge of the tape, or another halting state for a rejection.
- **Parser** turns a TSV machine file into a machine. It rejects files that break the format, with an error naming the offending line, and can also report warnings such as unreachable states.
- **Simulator** combines the parser and the machine: give it a machine file and an input, and it gives back the result.
- **Generator** produces the sorter's machine file.

## Using each tool

Run all commands from the `src` folder.

### Generator

Run the generator with the name of the file to create.

```sh
python Generator.py --output sorter.tsv
```

### Simulator

Run the simulator with a machine file and an input string. It prints the final state, the final tape and the final head position.

```sh
python Simulator.py --machine sorter.tsv --input '[0000000000000009,00000000000000A1,0000000000000002]'
```

## Running the tests

Install pytest.

```sh
pip install pytest
```

Then run tests in `src/test`:

```sh
python -m pytest test/*Test.py
```
