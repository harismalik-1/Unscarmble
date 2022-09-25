"""A simple checker for functions in unscramble_functions.py.

Copyright (c) 2021 Anya Tafliovich.
"""

from typing import Any, Dict
import unittest
import unscramble_functions as uf
import checker

MODULENAME = 'unscramble_functions'
PYTA_CONFIG = 'pyta/a1_pyta.txt'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'SHIFT': 'S',
    'SWAP': 'W',
    'CHECK': 'C'
}


class CheckTest(unittest.TestCase):
    """A simple checker (NOT a full tester!) for assignment functions."""

    def test_is_valid_move(self) -> None:
        """A simple check for is_valid_move."""

        self._check_simple_type(uf.is_valid_move,
                                ['C'],
                                bool)

    def test_get_section_start(self) -> None:
        """A simple check for get_section_start."""

        self._check_simple_type(uf.get_section_start,
                                [2, 3],
                                int)

    def test_get_section(self) -> None:
        """A simple check for get_section."""

        self._check_simple_type(uf.get_section,
                                ['cscisfun', 1, 4],
                                str)

    def test_is_valid_section(self) -> None:
        """A simple check for is_valid_section."""

        self._check_simple_type(uf.is_valid_section,
                                ['cscisfun', 1, 4],
                                bool)

    def test_swap(self) -> None:
        """A simple check for swap."""

        self._check_simple_type(uf.swap,
                                ['computerscience', 6, 10],
                                str)

    def test_shift(self) -> None:
        """A simple check for shift."""

        self._check_simple_type(uf.shift,
                                ['computerscience', 6, 10],
                                str)

    def test_check(self) -> None:
        """A simple check for function check."""

        self._check_simple_type(uf.check,
                                ['computerscience', 6, 10, 'computerscience'],
                                bool)

    def test_check_section(self) -> None:
        """A simple check for function check_section."""

        self._check_simple_type(uf.check_section,
                                ['computerscience', 1, 5, 'computerscience'],
                                bool)

    def test_change_section(self) -> None:
        """A simple check for function change_section."""

        self._check_simple_type(uf.change_section,
                                ['computerscience', 'W', 1, 5],
                                str)

    def test_get_move_hint(self) -> None:
        """A simple check for function get_move_hint."""

        self._check_simple_type(uf.get_move_hint,
                                ['TACDOGFOXEMU', 1, 3, 'CATDGOXOFEMU'],
                                str)

    def test_check_constants(self) -> None:
        """Check that values of constants are not changed."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, uf)
        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker.type_check_simple(func, args, expected)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_constants(self, name2value: Dict[str, Any], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.

        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


checker.ensure_no_io(MODULENAME)

print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker.run_pyta(MODULENAME + '.py', PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
