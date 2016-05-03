# todo: verify whether a molecule is valid or not; octet rule and stuff...
# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Atom:
    # An atom is an atom with up to four (or more) surrounding atoms and free electron pairs.
    def __init__(self):
        self.surrounding = list()


class Molecule:
    def __init__(self, formula=None, IUPAC=None, CAS=None):
        # examples for formula: 'Al2(SO4)3', 'CO2'
        # examples for IUPAC: 'aluminium sulfate', 'carbon dioxide'
        # examples for CAS: '10043-01-3', '124-38-9'
        if formula:
            self._parse_formula(formula)
        elif IUPAC:
            self._parse_IUPAC(IUPAC)
        elif CAS:
            self._get_CAS(CAS)

    def _add_atom(self, atom):
        if not atom:
            return
        print(atom)

    def _parse_formula(self, formula):
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

Molecule(formula='NaCO3')
