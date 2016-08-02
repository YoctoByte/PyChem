from molecules import Molecule


def formula(formula):
    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    prev_char = ''
    atom = ''
    for char in formula:
        if char.isupper():
            self._add_atom(atom)
            atom = char
        elif char.islower():
            atom = prev_char + char
        elif is_int(char):
            for _ in range(int(char)):
                self._add_atom(atom)
            atom = ''
        else:
            if char == '(':
                pass
            elif char == ')':
                pass
            else:
                raise ValueError(formula + ' is not a valid chemical formula.')
        prev_char = char
    if formula[-1].isupper() or formula[-1].islower():
        self._add_atom(atom)


def _parse_IUPAC(self, IUPAC):
    pass


def _get_CAS(self, CAS):
    pass