from atoms import Atom


def formula(formula_string):
    pass


def iupac(iupac_string):
    pass


def smiles(smiles_string):
    def tokenize(smiles_string):
        index = 0
        while index < len(smiles_string):
            if smiles_string[index] == '(':
                right_brack = index
                while True:
                    right_brack = smiles_string.find(')', right_brack) + 1
                    if right_brack == 0:
                        raise ValueError
                    bracketed_string = smiles_string[index:right_brack]
                    if bracketed_string.count('(') == bracketed_string.count(')'):
                        yield bracketed_string
                        index = right_brack
                        break
            elif smiles_string[index] == '[':
                right_brack = smiles_string.find(']', index) + 1
                if right_brack == 0:
                    raise ValueError
                yield smiles_string[index:right_brack]
                index = right_brack
            elif smiles_string[index] == '%':
                label_string = ''
                while True:
                    index += 1
                    if smiles_string[index] in '0123456789':
                        label_string += smiles_string[index]
                    else:
                        break
            else:
                yield smiles_string[index]
                index += 1

    def fill_hydrogen(molecule):
        return molecule

    molecule = set()
    labels = dict()
    last_atom = None
    bond_type = 'normal'
    for token in tokenize(smiles_string):
        if token in ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I']:
            new_atom = Atom(token)
            if last_atom:
                last_atom.add_bond(new_atom, bond_type)
                new_atom.add_bond(last_atom, bond_type)
            molecule.add(new_atom, bond_type)
            last_atom = new_atom
            bond_type = 'normal'
        elif isinstance(token, int):
            if token not in labels:
                labels[token] = last_atom
            else:
                labels[token].add_bond(new_atom, bond_type)
                new_atom.add_bond(labels[token], bond_type)
                bond_type = 'normal'
        elif token in ['=', '#', '$']:
            if token == '=':
                bond_type = 'double'
            elif token == '#':
                bond_type = 'triple'
            elif token == '$':
                bond_type = 'quadruple'
        elif token[0] == '(':
            new_molecule = smiles(token[1:-1])
        elif token[0] == '[':
            token = token[1:-1]
            element = None  # todo
            chirality = None
            charge = None

    return fill_hydrogen(molecule)


def cas(cas_string):
    pass


smiles('COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C')
#'[Cu+2].[O-]S(=O)(=O)[O-]')
# CC(=O)C
