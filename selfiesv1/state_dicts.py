"""A file of various state dictionaries used to enforce the SELFIES grammar in
a relatively fast manner.

Next steps include:
TODO: generate these _state_dicts and _state_library dynamically,
    using the above valence information.
TODO: For states 991-993, the new N state is 4, which is inconsistent with an
    unknown atom. Also, this can be expanded to pardon the restrictions on
    any atom in general.
"""

# Character State Dict Functions ===============================================

_state_dict_0 = {
    '[epsilon]': ('', 0),
    '[H]': ('[H]', 1),
    '[F]': ('F', 1),
    '[Cl]': ('Cl', 1),
    '[Br]': ('Br', 1),
    '[O]': ('O', 2),
    '[=O]': ('O', 2),
    '[N]': ('N', 3),
    '[=N]': ('N', 3),
    '[#N]': ('N', 3),
    '[NHexpl]': ('[NH]', 2),
    '[C]': ('C', 4),
    '[=C]': ('C', 4),
    '[#C]': ('C', 4),
    '[C@expl]': ('[C@]', 4),
    '[C@@expl]': ('[C@@]', 4),
    '[C@Hexpl]': ('[C@H]', 3),
    '[C@@Hexpl]': ('[C@@H]', 3),
    '[S]': ('S', 6),
    '[=S]': ('S', 6),
    '[???]': (None, 6)
}

_state_dict_1 = {
    '[epsilon]': ('', -1),
    '[H]': ('[H]', -1),
    '[F]': ('F', -1),
    '[Cl]': ('Cl', -1),
    '[Br]': ('Br', -1),
    '[O]': ('O', 1),
    '[=O]': ('O', -1),
    '[N]': ('N', 2),
    '[=N]': ('N', 2),
    '[#N]': ('N', 2),
    '[NHexpl]': ('[NH]', 1),
    '[C]': ('C', 3),
    '[=C]': ('C', 3),
    '[#C]': ('C', 3),
    '[C@expl]': ('[C@]', 3),
    '[C@@expl]': ('[C@@]', 3),
    '[C@Hexpl]': ('[C@H]', 2),
    '[C@@Hexpl]': ('[C@@H]', 2),
    '[S]': ('S', 5),
    '[=S]': ('S', 5),
    '[???]': (None, 6)
}

_state_dict_2 = {
    '[epsilon]': ('', -1),
    '[H]': ('[H]', -1),
    '[F]': ('F', -1),
    '[Cl]': ('Cl', -1),
    '[Br]': ('Br', -1),
    '[O]': ('O', 1),
    '[=O]': ('=O', -1),
    '[N]': ('N', 2),
    '[=N]': ('=N', 1),
    '[#N]': ('=N', 1),
    '[NHexpl]': ('[NH]', 1),
    '[C]': ('C', 3),
    '[=C]': ('=C', 2),
    '[#C]': ('=C', 2),
    '[C@expl]': ('[C@]', 3),
    '[C@@expl]': ('[C@@]', 3),
    '[C@Hexpl]': ('[C@H]', 2),
    '[C@@Hexpl]': ('[C@@H]', 2),
    '[S]': ('S', 5),
    '[=S]': ('=S', 4),
    '[???]': (None, 6)
}

_state_dict_3_to_6 = {
    '[epsilon]': ('', -1),
    '[H]': ('[H]', -1),
    '[F]': ('F', -1),
    '[Cl]': ('Cl', -1),
    '[Br]': ('Br', -1),
    '[O]': ('O', 1),
    '[=O]': ('=O', -1),
    '[N]': ('N', 2),
    '[=N]': ('=N', 1),
    '[#N]': ('#N', -1),
    '[NHexpl]': ('[NH]', 1),
    '[C]': ('C', 3),
    '[=C]': ('=C', 2),
    '[#C]': ('#C', 1),
    '[C@expl]': ('[C@]', 3),
    '[C@@expl]': ('[C@@]', 3),
    '[C@Hexpl]': ('[C@H]', 2),
    '[C@@Hexpl]': ('[C@@H]', 2),
    '[S]': ('S', 5),
    '[=S]': ('=S', 4),
    '[???]': (None, 6)
}

# <_state_library> is accessed through two keys, which are (1) the current
# derivation state and (2) the current SELFIES character to be derived, or
# '[???]' is the character is unknown. The corresponding value is a tuple of
# (1) the derived SMILES character, and (2) the next derivation state.

_state_library = {
    0: _state_dict_0,
    1: _state_dict_1,
    2: _state_dict_2,
    3: _state_dict_3_to_6,
    4: _state_dict_3_to_6,
    5: _state_dict_3_to_6,
    6: _state_dict_3_to_6,
    9991: _state_dict_1,
    9992: _state_dict_2,
    9993: _state_dict_3_to_6
}


def get_next_state(char, state, N_restrict):
    """Given the current non-branch, non-ring character and current derivation
    state, retrieves the derived SMILES character and the next derivation state.

    Args:
        char: a SELFIES character that is not a Ring or Branch
        state: the current derivation state
        N_restrict: if True, nitrogen is restricted to 3 bonds

    Returns: a tuple of (1) the derived character, and (2) the
             next derivation state
    """

    state_dict = _state_library[state]

    if char in state_dict:
        derived_char, new_state = state_dict[char]

        # relax nitrogen constraints if N_restrict = False
        if not N_restrict and (char in ['[N]', '[=N]', ['#N']]):
            _, new_state = state_dict['[???]']

            if state >= 991:
                new_state = 4

        return derived_char, new_state

    else:  # unknown SELFIES character
        _, new_state = state_dict['[???]']
        derived_char = _process_unknown_char(char)
        return derived_char, new_state


# <_bracket_less_smiles> is a set of SELFIES symbols, whose
# SMILES counterparts cannot have brackets by convention.

_bracket_less_smiles = {'[B]', '[C]', '[N]', '[P]', '[O]', '[S]',
                        '[F]', '[Cl]', '[Br]', '[I]',
                        '[c]', '[n]', '[o]', '[s]', '[p]'}


def _process_unknown_char(char):
    """Attempts to convert an unknown SELFIES character <char> into a
    proper SMILES character. For example, explicit aromatic symbols
    are not part of the SELFIES alphabet, but _process_unknown_char
    will help convert [c], [n], [o] --> c, n, o.

    Args:
        char: an unknown SELFIES character

    Returns: the processed SMILES character
    """

    processed = ""

    if char[0: 2] in ('[=', '[#', '[\\', '[/', '[-'):
        processed += char[1]
        char = "[" + char[2:]

    if char in _bracket_less_smiles:
        char = char[1: -1]  # remove [ and ] brackets

    if 'expl' in char:
        char = char.replace('expl]', ']')

    processed += char

    return processed


# Branch State Dict Functions ==================================================

# <_branch_state_library> takes as a key the current derivation state.
# Its value is a tuple; for [BranchL_X], the (X - 1)th element of the tuple
# gives a tuple of (1) the initial branch derivation state and (2) the
# next derivation state (after the branch is derived).

_branch_state_library = {
    0: ((None, 0), (None, 0), (None, 0)),
    1: ((None, 1), (None, 1), (None, 1)),
    2: ((9991, 1), (9991, 1), (9991, 1)),
    3: ((9991, 2), (9991, 2), (9992, 1)),
    4: ((9992, 2), (9991, 3), (9993, 1)),
    5: ((9992, 3), (9991, 4), (9993, 2)),
    6: ((9992, 4), (9991, 5), (9993, 3)),
    9991: ((None, 9991), (None, 9991), (None, 9991)),
    9992: ((None, 9992), (None, 9992), (None, 9992)),
    9993: ((None, 9993), (None, 9993), (None, 9993))
}


def get_next_branch_state(branch_char, state):
    """Given the branch character and current derivation state, retrieves
    the initial branch derivation state (i.e. the derivation state that the
    new branch begins on), and the next derivation state (i.e. the derivation
    state after the branch is created).

    Args:
        branch_char: the branch character (e.g. [Branch1_2], [Branch3_1])
        state: the current derivation state

    Returns: a tuple of (1) the initial branch state and (2) the next state
    """

    branch_type = int(branch_char[-2])  # branches are of the form [BranchL_X]

    if not (1 <= branch_type <= 3):
        raise ValueError(f"Unknown branch character: {branch_char}")

    return _branch_state_library[state][branch_type - 1]


# SELFIES Character to N Functions =============================================

_index_alphabet = ['[epsilon]', '[Ring1]', '[Ring2]',
                   '[Branch1_1]', '[Branch1_2]', '[Branch1_3]',
                   '[Branch2_1]', '[Branch2_2]', '[Branch2_3]',
                   '[F]', '[O]', '[=O]', '[N]', '[=N]', '[#N]',
                   '[C]', '[=C]', '[#C]', '[S]', '[=S]']

# <_alphabet_code> takes as a key a SELFIES char, and its corresponding value
# is the index of the key.

_alphabet_code = {c: i for i, c in enumerate(_index_alphabet)}


def get_chars_index(*chars, default=1):
    """Converts a list of SELFIES characters [c_1, ..., c_n] into a number N.
    This is done by converting each character c_n to an integer idx(c_n) via
    <_alphabet_code>, adding 1 to the first integer idx(c_1), and then treating
    the list as a number in base len(_alphabet_code).

    Args:
        *chars: a list of SELFIES characters
        default: the value to be returned if an error occurs.

    Returns: the corresponding N for <chars>, or <default> if an element
             in <chars> does not have an index.
    """

    if any(c not in _alphabet_code for c in chars):
        return default

    N = 0
    for i, c in enumerate(reversed(chars)):
        N_i = _alphabet_code[c] + int(i == len(chars) - 1)
        N_i *= (len(_alphabet_code) ** i)
        N += N_i
    return N

