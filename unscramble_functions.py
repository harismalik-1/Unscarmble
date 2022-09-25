"""CSC108/A08: Fall 2021 -- Assignment 1: unscramble

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Anya Tafliovich.

"""

# Valid moves in the game.
SHIFT = 'S'
SWAP = 'W'
CHECK = 'C'


# We provide a full solution to this function as an example.
def is_valid_move(move: str) -> bool:
    """Return True if and only if move is a valid move. Valid moves are
    SHIFT, SWAP, and CHECK.

    >>> is_valid_move('C')
    True
    >>> is_valid_move('S')
    True
    >>> is_valid_move('W')
    True
    >>> is_valid_move('R')
    False
    >>> is_valid_move('')
    False
    >>> is_valid_move('NOT')
    False

    """

    return move == CHECK or move == SHIFT or move == SWAP

# Your turn! Provide full solutions to the rest of the required functions.


def get_section_start(sect_nm: int, sect_ln: int) -> int:
    """Return the index of the first character in the specified section with
    section number in sect_nm and section length in sect_ln.

    precondition: sect_nm >= 1
                 sect_len >= 1

    >>> get_section_start(1,4)
    0
    >>> get_section_start(3,4)
    8
    >>> get_section_start(2,3)
    3
    >>> get_section_start(3,3)
    6

    """

    return sect_nm * sect_ln - sect_ln

def get_section(scram: str, sect_nm: int, sect_ln: int) -> str:
    """Return the section of the state that corresponds to the given
    section number in sect_num by slicing it from the given string in scram.

    precondition: sect_num and sect_ln are valid for the given scram

    >>> get_section('csca08fun', 2, 3)
    'a08'
    >>> get_section('governor', 3, 2)
    'rn'
    >>> get_section('disagreeable', 2, 4)
    'gree'

    """
    first_index = get_section_start(sect_nm, sect_ln)
    second_index = get_section_start(sect_nm, sect_ln) + sect_ln

    return scram[first_index: second_index]

def is_valid_section(scram: str, sect_nm: int, sect_ln: int) -> bool:
    """Return True if and only if it is possible to divide up the given
    scambled string into sections of the given length in sect_ln and the
    given section number in sect_nm.

    precondition: sect_nm >= 1
                 sect_len >= 1

    >>> is_valid_section('csca08fall2021', 2, 3)
    False
    >>> is_valid_section('csca08fall2021', 4, 2)
    True
    >>> is_valid_section('csca08fall2021', 8, 2)
    False

    """
    first_test = len(scram) % sect_ln == 0
    second_test = sect_nm <= len(scram) / sect_ln

    return first_test and second_test


def swap(scram: str, start_index: int, end_index: int) -> str:
    """ Return a string which is the result of applying a Swap operation on
    the section of the given state string in sect_nm to swap the character at
    start index with the character at one before the end index.

    precondition: start_index and end_index are valid for given scram
                 start_index < end_index - 1

    >>> swap('computerscience', 0, 8)
    'romputecscience'
    >>> swap('computerscience', 6, 10)
    'computcrseience'
    >>> swap('Haris', 2, 5)
    'Hasir'
    """
    first_part = scram[0:start_index]
    swap_ch = scram[end_index -1]
    middle_part = scram[start_index + 1: end_index - 1]
    swap_ch2 = scram[start_index]
    last_part = scram[end_index:]


    return first_part + swap_ch + middle_part + swap_ch2 + last_part


def shift(scram: str, start_index: int, end_index: int) -> str:
    """Return a string which is the result of applying a Shift operation to
    the section of the given state string in sect_num to shift the character at
    the start index to one place before the end index.

    precondition: start_index and end_index are valid for given scram
                 start_index < end_index - 1

    >>> shift('computerscience', 0, 8)
    'omputercscience'
    >>> shift('computerscience', 6, 10)
    'computrsceience'

    """
    first_part = scram[0: start_index]
    middle_part = scram[start_index + 1: end_index]
    shift_ch = scram[start_index]
    last_part = scram[end_index:]

    return first_part + middle_part + shift_ch + last_part

def check(scram: str, start_index: int, end_index: int, unscram: str) -> bool:
    """Return True if and only if the part of the state string traced in
    between the start index (inclusive) and the end index (exclusive) is
    correct when compared with the unscrambled string in unscram.

    precondition: start_index and end_index are valid for given scram
                 start_index <= end_index
                 unscram is a valid answer to the scrambled string in scram

    >>> check('ccsa80fun', 6, 9, 'csca08fun')
    True
    >>> check('ccsa80fun', 0, 3, 'csca08fun')
    False

    """

    return scram[start_index: end_index] in unscram


def check_section(scram: str, sect_nm: int, sect_ln: int, unscram: str) -> bool:
    """Return True if and only if the section with the specified section
    number in sect_nm is equal to the section in the unscrambled string stored
    in unscram.

    precondition: sect_nm and sect_ln are valid for given scram
                 unscram is a valid answer to the scrambled string in scram

    >>> check_section('ccsa80fun', 3, 3, 'csca08fun')
    True
    >>> check_section('ccsa80fun', 1, 3, 'csca08fun')
    False

    """

    return get_section(scram, sect_nm, sect_ln) in unscram


def change_section(scram: str, game_mv: str, sect_nm: int, sect_ln: int) -> str:
    """Return a new game state which results from applying the given game move
    that is either SHIFT or SWAP on the section with the given section number
    in sect_nm.

    precondition: sect_nm and sect_ln are valid for given scram
                 game_mv is a valid game move that specifies either SWIFT or
                 SWAP

    >>> change_section('computerscience', 'W', 2, 5)
    'compucerstience'
    >>> change_section('computerscience', 'S', 3, 5)
    'computerscencei'

    """
    start_index = get_section_start(sect_nm, sect_ln)
    end_index = sect_nm * sect_ln

    if game_mv == 'W':
        return swap(scram, start_index, end_index)
    if game_mv == 'S':
        return shift(scram, start_index, end_index)
    return ''

def get_move_hint(scram: str, sect_nm: int, sect_ln: int, unscram: str) -> str:
    """Return a suggestion for the given scrambled string in scram to which
    game move that is either SHIFT or SWAP to perform next in order to
    unscramble the given string by comparing it with unscram.

    precondition: sect_nm and sect_ln are valid for given scram
                 unscram is a valid answer to the scrambled string in scram


    >>> get_move_hint('ccsa08fun', 1, 3, 'csca08fun')
    'S'
    >>> get_move_hint('csc0a8fun', 2, 3, 'csca08fun')
    'W'

    """
    start_index = get_section_start(sect_nm, sect_ln)
    end_index = sect_nm * sect_ln
    new_scram = shift(scram, start_index, end_index)

    if shift(scram, start_index, end_index) == unscram:
        return SHIFT
    if shift(new_scram, start_index, end_index) == unscram:
        return SHIFT
    return SWAP


if __name__ == '__main__':
    import doctest
    doctest.testmod()
