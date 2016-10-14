from pychem.molecule.molecule import Molecule, Atom, Bond


def parse(smiles_string, molecule=None):
    if molecule is None:
        molecule = Molecule()
    _parse_from_smiles(molecule, smiles_string)
    for atom in molecule.atoms.copy():
        atom.fill_hydrogen()
    return molecule


def _parse_from_smiles(molecule, smiles_string, _active_atom=None, _labels=None):
    active_atom = _active_atom
    if _labels is None:
        labels = dict()
    else:
        labels = _labels

    bond_type = '-'
    for token in _tokenize_smiles(smiles_string):
        if token[0] == '(':
            _parse_from_smiles(molecule, token[1:-1], _active_atom=active_atom, _labels=labels)
        elif token[0] == '[':
            isotope, element, h_count, charge, chirality = _parse_smiles_parenthesis(token)
            new_atom = Atom(element, molecule, isotope=isotope, charge=charge, aromatic=element.islower())
            new_atom.h_count = h_count
            molecule.add_atom(new_atom)
            if active_atom:
                bond = Bond(active_atom, new_atom, bond_type=bond_type)
                molecule.add_bond(bond)
            active_atom = new_atom
            bond_type = '-'
        elif token.lower() in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
            new_atom = Atom(token, molecule, aromatic=token.islower())
            molecule.add_atom(new_atom)
            if active_atom:
                bond = Bond(active_atom, new_atom, bond_type=bond_type)
                molecule.add_bond(bond)
            active_atom = new_atom
            bond_type = '-'
        elif token[0] == '%':
            label = token[1:]
            if label not in labels:
                labels[label] = active_atom
            else:
                bond = Bond(active_atom, labels[label], bond_type=bond_type)
                molecule.add_bond(bond)
                bond_type = '-'
        elif token in ['-', '=', '#', '$', ':']:
            bond_type = token


def _tokenize_smiles(smiles_string):
    index = 0
    while index < len(smiles_string):
        if smiles_string[index] == '(':
            right_brack = index
            while index < len(smiles_string):
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
            label_string = '%'
            while index + 1 < len(smiles_string):
                index += 1
                if smiles_string[index] in '0123456789':
                    label_string += smiles_string[index]
                else:
                    break
            yield label_string
        else:
            if smiles_string[index] in '0123456789':
                yield '%' + smiles_string[index]
            else:
                element_string = smiles_string[index]
                if index+1 < len(smiles_string) and smiles_string[index+1].islower():
                    element_string += smiles_string[index+1]
                    index += 1
                yield element_string
            index += 1


def _parse_smiles_parenthesis(token):
    token = token[1:-1]
    token = token.replace(' ', '')

    isotope = None
    element = ''
    h_count = 0
    charge = 0
    chirality = ''

    index = 0
    # parse the isotope from the token:
    isotope_string = ''
    while index < len(token) and token[index] in '0123456789':
        isotope_string += token[index]
        index += 1
    if isotope_string:
        isotope = int(isotope_string)
    # parse the element from the token:
    while index < len(token) and token[index].isalpha():
        if element and token[index] == 'H':
            break
        element += token[index]
        index += 1
    # parse the hydrogen count from the token:
    if index < len(token) and token[index] == 'H':
        index += 1
        h_count_string = ''
        while index < len(token) and token[index] in '0123456789':
            h_count_string += token[index]
            index += 1
        if h_count_string:
            h_count = int(h_count_string)
    # parse the charge from the token:
    if index < len(token) and token[index] in '-+':
        charge_string = ''
        while index < len(token) and token[index] in '-+0123456789':
            charge_string += token[index]
            index += 1
        try:
            charge = int(charge_string[1:])
            if charge_string[0] == '-':
                charge *= -1
        except ValueError:
            charge = charge_string.count('+') - charge_string.count('-')
    # parse the chirality from the token:
    if index < len(token) and token[index] == '@':
        chirality += '@'
        index += 1
        if index < len(token) and token[index] == '@':
            chirality += '@'
            index += 1
        if index+1 < len(token) and token[index:index+2] in ['TH', 'AL', 'SP', 'TB', 'OH']:
            # TH: Tetrahedral, AL: Allenal, SP: Square Planar, TB: Trigonal Bipyramidal, OH: Octahedral
            chirality += token[index:index+2]

    return isotope, element, h_count, charge, chirality
