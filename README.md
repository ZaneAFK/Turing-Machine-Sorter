# Turing-Machine-Sorter

A toolchain for building and testing a Turing machine that sorts a list of 16-digit hex words.

The sorter is written in the 41080 Theory of Computing Science course's Turing Machine Specification Format, a five-column tab-separated (TSV) file. The TSV file is the turing machine which is produced by `Generator.py`.

## Repository structure

```
.
├── README.md
└── src/
    ├── Generator.py        writes the sorter's machine file
    ├── tm_reference/       the course's reference checker and simulator
    │   ├── tm.py           checks machine files and runs them
    │   ├── README.txt      the reference tool's own documentation
    │   ├── examples/       valid machine files
    │   └── broken/         invalid or questionable machine files
    └── test/
        └── GeneratorTest.py  tests for the generated sorter
```

- **Generator** produces the sorter's machine file.
- **tm_reference** is the tutor's checker and simulator. It is the canonical definition of the machine file format, so it decides whether the generated file is valid and what it does. It is not modified here.
- **GeneratorTest** checks the generated sorter by running it with the reference simulator.

## Using each tool

Run all commands from the `src` folder.

### Generator

Run the generator with the name of the file to create.

```sh
python Generator.py --output sorter.tsv
```

### Checker and simulator

The course's reference tool checks a machine file and runs it on one or more input strings. It prints whether the file is valid, then the final state, the number of steps and the final tape for each input. Quote each input so the shell does not interpret the brackets.

```sh
python tm_reference/tm.py sorter.tsv '[0000000000000009,00000000000000A1,0000000000000002]'
```

Run it with just a machine file to check the file without running it. See `src/tm_reference/README.txt` for its other options.

## Running the tests

Install pytest.

```sh
pip install pytest
```

Then run tests in `src/test`:

```sh
python -m pytest test/*Test.py
```
