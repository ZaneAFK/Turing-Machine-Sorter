import random

import pytest

import Generator
from tm_reference import tm

HEX = '0123456789ABCDEF'

def tape_of(final):
    return tm.tape_string(final)


@pytest.fixture(scope='module')
def tsv():
    return Generator.GenerateTSV()


@pytest.fixture(scope='module')
def machine(tsv):
    machine, _ = tm.parse(tsv.encode('utf-8'))
    return machine


class TestGenerateTSV:
    def test_valid_with_no_warnings(self, tsv):
        _, warnings = tm.parse(tsv.encode('utf-8'))
        assert warnings == []

class TestSorting:
    def test_empty_list(self, machine):
        final = tm.run(machine, '[]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[]'

    def test_one_word(self, machine):
        final = tm.run(machine, '[0123456789ABCDEF]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0123456789ABCDEF]'

    def test_two_in_order(self, machine):
        final = tm.run(machine, '[0000000000000001,0000000000000002]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000001,0000000000000002]'

    def test_two_out_of_order(self, machine):
        final = tm.run(machine, '[0000000000000002,0000000000000001]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000001,0000000000000002]'

    def test_all_equal(self, machine):
        word = 'ABCDEF0123456789'
        final = tm.run(machine, f'[{word},{word},{word},{word},{word},{word}]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == f'[{word},{word},{word},{word},{word},{word}]'

    def test_duplicates_mixed(self, machine):
        final = tm.run(machine, '[FFFFFFFFFFFFFFFF,0000000000000001,0000000000000A00,0000000000000001,'
                                'FFFFFFFFFFFFFFFF,0000000000000A00,0000000000000001]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == ('[0000000000000001,0000000000000001,0000000000000001,'
                                         '0000000000000A00,0000000000000A00,FFFFFFFFFFFFFFFF,FFFFFFFFFFFFFFFF]')

    def test_already_sorted(self, machine):
        words = [f'{i:016X}' for i in range(40)]
        final = tm.run(machine, '[' + ','.join(words) + ']')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[' + ','.join(words) + ']'

    def test_reverse_sorted(self, machine):
        words = [f'{i:016X}' for i in range(40)]
        final = tm.run(machine, '[' + ','.join(reversed(words)) + ']')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[' + ','.join(words) + ']'

    def test_first_digit_only_differs(self, machine):
        final = tm.run(machine, '[F000000000000000,0000000000000000,9000000000000000,A000000000000000]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000000,9000000000000000,A000000000000000,F000000000000000]'

    def test_last_digit_only_differs(self, machine):
        final = tm.run(machine, '[000000000000000F,0000000000000000,0000000000000009,000000000000000A]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000000,0000000000000009,000000000000000A,000000000000000F]'

    def test_nine_versus_A(self, machine):
        final = tm.run(machine, '[000000000000000A,0000000000000009]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000009,000000000000000A]'

    def test_F_before_0(self, machine):
        final = tm.run(machine, '[FFFFFFFFFFFFFFFF,0000000000000000]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000000,FFFFFFFFFFFFFFFF]'

    def test_0_before_F(self, machine):
        final = tm.run(machine, '[0000000000000000,FFFFFFFFFFFFFFFF]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000000,FFFFFFFFFFFFFFFF]'

    def test_worked_example(self, machine):
        final = tm.run(machine, '[0000000000000009,00000000000000A1,0000000000000002]')
        assert final.state == '✔'
        assert final.head == 0
        assert tape_of(final) == '[0000000000000002,0000000000000009,00000000000000A1]'

    def test_random_lists_full_alphabet(self, machine):
        rng = random.Random(5)
        for _ in range(300):
            words = [''.join(rng.choice(HEX) for _ in range(16)) for _ in range(rng.randint(2, 12))]
            final = tm.run(machine, '[' + ','.join(words) + ']')
            assert final.state == '✔', words
            assert final.head == 0, words
            assert tape_of(final) == '[' + ','.join(sorted(words)) + ']', words
