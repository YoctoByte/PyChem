from molecules import Molecule
from atoms import Atom


def formula(formula_string):
    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    prev_char = ''
    atom = ''
    for char in formula_string:
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
                raise ValueError(formula_string + ' is not a valid chemical formula.')
        prev_char = char
    if formula_string[-1].isupper() or formula_string[-1].islower():
        self._add_atom(atom)


def iupac(iupac_string):
    pass


def smiles(smiles_string):
    def tokenize(smiles_string):
        index = 0
        while index < len(smiles_string):
            if smiles_string[index] == '(':
                right_brack = index
                while True:
                    right_brack = smiles_string.find(')', right_brack)
                    if right_brack == -1:
                        raise ValueError
                    bracketed_string = smiles_string[index:right_brack+1]
                    if bracketed_string.count('(') == bracketed_string.count(')'):
                        yield bracketed_string
                        index = right_brack + 1
                        break
            elif smiles_string[index] == '[':
                right_brack = smiles_string.find(']', index) + 1
                if right_brack == 0:
                    raise ValueError
                yield smiles_string[index:right_brack]
                index = right_brack
            elif smiles_string[index] == '@':
                if smiles_string[index+1] == '@':
                    yield '@@'
                    index += 2
                else:
                    yield '@'
                    index += 1
            else:
                yield smiles_string[index]
                index += 1

    def fill_hydrogen(molecule):
        return molecule

    molecule = list()
    labels = dict()
    for token in tokenize(smiles_string):
        if token in ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I']:
            new_atom = Atom(token)
            if molecule:
                molecule[-1].surroundings.append(new_atom)
                new_atom.surroundings.append(molecule[-1])
            molecule.append(new_atom)
        if isinstance(token, int):
            if token not in labels:
                labels[token] = molecule[-1]
            else:
                labels[token].surroundings.append(new_atom)
                new_atom.surroundings.append(labels[token])

    return fill_hydrogen(molecule)


def cas(cas_string):
    pass


smiles('CN=C=O')
# CC(=O)C