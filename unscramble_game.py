"""CSC108/A08: Fall 2021 -- Assignment 1: unscramble

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Anya Tafliovich.

"""

import random
import unscramble_functions as uf
from typing import Tuple

TEST_MODE = 'T'
NORMAL_MODE = 'N'
HINT_MODE = 'H'

YES = 'Y'
NO = 'N'

WORDS_FILE = 'words.txt'


def setup_game() -> Tuple[str, int]:
    """Randomly generate a word and a section length. Return a pair (word,
    section length).

    A word is randomly selected from the file WORDS_FILE. A section
    length is randomly selected among valid section lengths (of at
    least 2) for the chosen word.

    """

    # choose a random word from the input words file
    with open(WORDS_FILE) as words_file:
        answer = random.choice(words_file.readlines()).strip()

    # generate a random valid section length between 2 and len(answer)/2
    # (all words in our input file are of non-prime length)
    max_len = len(answer) // 2
    section_len = random.choice([i for i in range(2, max_len + 1)
                                 if len(answer) % i == 0])

    return (answer, section_len)


def scramble(word: str, section_len: int) -> str:
    """Return a scrambled version of word. The scrambling is done by
    dividing word into sections of length section_len and randomly
    shuffling each section.

    Pre: len(word) is a multiple of section_len
         section_len >= 2

    """

    scrambled = ''
    for i in range(len(word) // section_len):
        section = list(word[section_len * i: section_len * (i + 1)])
        random.shuffle(section)
        scrambled += ''.join(section)
    return scrambled


def is_valid_mode(mode: str) -> bool:
    """Return True if and only if mode is a valid mode.

    >>> is_valid_mode('T')
    True
    >>> is_valid_mode('N')
    True
    >>> is_valid_mode('H')
    True
    >>> is_valid_mode('S')
    False
    >>> is_valid_mode('')
    False
    """

    return mode in (TEST_MODE, NORMAL_MODE, HINT_MODE)


def in_test_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in test mode.

    >>> in_test_mode('T')
    True
    >>> in_test_mode('N')
    False
    """

    return mode == TEST_MODE


def in_hint_mode(mode: str) -> bool:
    """Return True if and only if mode indicates the game is in hint mode.

    >>> in_hint_mode('H')
    True
    >>> in_hint_mode('N')
    False
    """

    return mode == HINT_MODE


def get_mode() -> str:
    """Prompt user repeatedly to enter a valid game mode. Return the
    entered game mode.

    """

    msg = 'Enter the mode to play [{}: test, {}: normal, {}: hint]: '.format(
        TEST_MODE, NORMAL_MODE, HINT_MODE)
    mode = input(msg).upper()
    while not is_valid_mode(mode):
        print('Invalid mode!')
        mode = input(msg).upper()
    return mode


def get_section_number(state: int, section_len: int) -> int:
    """Prompt user repeatedly to enter a valid section number for state
    and section length section_len. Return the entered section number.

    Pre: section_len is valid section length for state

    """

    msg = 'Enter a section number: '
    section_num = input(msg)
    while not (section_num.isdigit() and
               uf.is_valid_section(state, int(section_num), section_len)):
        print('Invalid section number!')
        section_num = input(msg)
    return int(section_num)


def get_move() -> str:
    """Prompt user repeatedly to enter a valid move. Return the entered
    move.

    """

    msg = 'Enter a move  [{}: check, {}: shift, {}: swap): '.format(
        uf.CHECK, uf.SHIFT, uf.SWAP)
    move = input(msg).upper()
    while not uf.is_valid_move(move):
        print('Invalid move!')
        move = input(msg).upper()
    return move


def make_move(state: str, section_num: int, move: str, section_len: int,
              answer: str) -> str:
    """Return the new game state after performing the game move specified
    by move on the section of state correspoding to section_num, with
    section length section_len and corect answer to the game
    answer. If move is unscramble_functions.CHECK, display whether the
    section is correctly solved.

    Pre: section_num is a valid section number in state
         section_len is a valid section length for state
         answer is a valid asnwer for state
         move is a valid move

    >>> make_move('TCADOGFOXEMU', 1, 'S', 3, 'CATDOGFOXEMU')
    'CATDOGFOXEMU'
    >>> make_move('CATDOGFOXUME', 4, 'C',  3, 'CATDOGFOXEMU')
    The section is incorrect
    'CATDOGFOXUME'
    >>> make_move('CATDOGFOXUME', 2, 'C',  3, 'CATDOGFOXEMU')
    The section is correct
    'CATDOGFOXUME'

    """

    if move == uf.CHECK:
        check_result = uf.check_section(
            state, section_num, section_len, answer)
        if check_result:
            print('The section is correct')
        else:
            print('The section is incorrect')
    else:
        state = uf.change_section(state, move, section_num, section_len)
    return state


def section_hint(state: str, section_len: int, answer: str) -> int:
    """Return a random section number corresponding to a section of state
    that is not correctly arranged, given the length of each section
    section_len and the correct answer answer.

    Pre: section_len is a valid section length for state
         answer is a valid answer for state
         state is not completely solved

    >>> section_hint('ATCDOGFOXEMU', 3, 'CATDOGFOXEMU')
    1
    >>> section_hint('CATDGOFOXEMU', 3, 'CATDOGFOXEMU')
    2
    >>> section_hint('CATDOGXOFEMU', 3, 'CATDOGFOXEMU')
    3
    >>> section_hint('CATDOGFOXMUE', 3, 'CATDOGFOXEMU')
    4

    """

    return random.choice([i + 1 for i in range(len(state) // section_len)
                         if not uf.check_section(state, i + 1,
                                                 section_len, answer)])


def get_section_hint(state: str, section_len: int, answer: str) -> int:
    """Return the number of hints given (0 or 1).

    Ask the user if they want a section hint. If yes, display the
    hint.

    Pre: section_len is a valid section length for state
         answer is a valid asnwer for state

    """

    hint = input('Would you like a section hint ({}/{}): '.format(YES, NO))
    if hint.upper() == YES:
        print('Your section hint is: {}'.format(
            section_hint(state, section_len, answer)))
        return 1
    return 0


def get_move_hint(state: str, section_num: int, section_len: int,
                  answer: str) -> int:
    """Return the number of hints given (0 or 1).

    Ask the user if they want a move hint. If they do, offer a hint.

    Pre: section_num is a valid section number in state
         section_len is a valid section length for state
         answer is a valid asnwer for state
    """

    hint = input('Would you like a move hint ({}/{}): '.format(YES, NO))
    if hint.upper() == YES:
        print('Your move hint is: {}'.format(
              uf.get_move_hint(state, section_num, section_len, answer)))
        return 1
    return 0


def play_game(state: str, mode: str, section_len: int, answer: str) -> int:
    """Return the number of moves taken to arrive at the correct answer.
    Run the main loop in game-mode mode, prompting the user for input
    and consequently updating state. Note that each hint costs a move.

    Pre: section_len is a valid section length for state
         answer is a valid asnwer for state
         mode is a valid game mode

    """

    if in_test_mode(mode):
        print('Answer: ' + answer)

    moves = 0
    while state != answer:
        print('Current state: {}. Section length: {}.'.format(
            state, section_len))

        if in_hint_mode(mode):
            moves += get_section_hint(state, section_len, answer)
        section_num = get_section_number(state, section_len)

        if in_hint_mode(mode):
            moves += get_move_hint(state, section_num, section_len, answer)
        move = get_move()

        state = make_move(state, section_num, move, section_len, answer)
        moves += 1
    return moves


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    answer, section_len = setup_game()
    start_state = scramble(answer, section_len)
    game_mode = get_mode()
    num_moves = play_game(start_state, game_mode, section_len, answer)
    print('You won the game in {} moves! The answer is {}.'.format(
        num_moves, answer))
