from pychem.molecules.atom import Atom
from pychem.molecules.bond import Bond


def parse_from(molecule, smiles_string):
    # todo: process / and \ , ie: F/C=C/Cl
    # todo: process chirality, ie: @/@@, AL/TH, 1/2
    # todo: process hydrogen count

    atoms = set()
    bonds = set()

    if molecule is None:
        is_side_chain = True
    else:
        is_side_chain = False
    first_atom = None
    first_bond_type = '-'

    active_atom = None
    bond_type = '-'
    for token in _tokenize(smiles_string):
        if token.lower() in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
            new_atom = Atom(token)
            if token in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
                new_atom.aromatic = True
            if not first_atom:
                first_atom = new_atom
            if active_atom:
                bonds.add(Bond(atoms={active_atom, new_atom}, bond_type=bond_type))
            atoms.add(new_atom)
            active_atom = new_atom
            bond_type = '-'
        elif token[0] == '%':
            bonds.add(Bond(atoms={active_atom, token[1:]}, bond_type=bond_type))
            bond_type = '-'
        elif token in ['-', '=', '#', '$', ':']:  # todo: process / and \ , ie: F/C=C/Cl
            bond_type = token
            if not first_atom:
                first_bond_type = token
        elif token[0] == '(':
            side_chain = parse_from(None, token[1:-1])
            atoms.update(side_chain['atoms'])
            bonds.update(side_chain['bonds'])
            bonds.add(Bond(atoms={active_atom, side_chain['first_atom']}, bond_type=side_chain['first_bond_type']))
        elif token[0] == '[':
            isotope, element, h_count, charge, chirality = _parse_parenthesis(token)
            new_atom = Atom(element)
            if isotope:
                new_atom.isotope = isotope
            if charge:
                new_atom.charge = charge
            if element in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
                new_atom.aromatic = True
            if not first_atom:
                first_atom = new_atom
            if active_atom:
                bonds.add(Bond(atoms={active_atom, new_atom}, bond_type=bond_type))
            # todo: process chirality, ie: @/@@, AL/TH, 1/2
            # todo: process hydrogen count
            atoms.add(new_atom)
            active_atom = new_atom
            bond_type = '-'

    if is_side_chain:
        side_chain = {'atoms': atoms, 'bonds': bonds, 'first_atom': first_atom, 'first_bond_type': first_bond_type}
        return side_chain
    else:
        bonds = _connect_bonds(bonds)
        atoms, bonds = _fill_hydrogen(atoms, bonds)
        molecule.atoms = atoms
        molecule.bonds = bonds
        return molecule


# def parse_to(molecule):
#     pass


def _tokenize(smiles_string):
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
            label_string = '%'
            while True:
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
                yield smiles_string[index]
            index += 1


def _parse_parenthesis(token):
    token = token[1:-1]
    token = token.replace(' ', '')

    isotope = 0
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
        else:
            h_count = 1
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


def _connect_bonds(bonds):
    labels = dict()
    new_bonds = set()
    for bond in bonds:
        new_bonds.add(bond)
        for label in bond.atoms:
            if isinstance(label, str):
                new_bonds.remove(bond)
                atoms_copy = bond.atoms.copy()
                atoms_copy.remove(label)
                atom = atoms_copy.pop()
                if label not in labels:
                    labels[label] = atom
                else:
                    new_bonds.add(Bond(atoms={atom, labels[label]}))
    return new_bonds


def _fill_hydrogen(atoms, bonds):
    return atoms, bonds


def _find_longest_chain(self):
    def remove_unused_bonds(atoms, bonds):
        new_bonds = set()
        for bond in bonds:
            do_not_add = False
            for atom in bond.atoms:
                if atom not in atoms:
                    do_not_add = True
                    break
            if not do_not_add:
                new_bonds.add(bond)
        return new_bonds

    def recursive(current_chain, bonds):
        print('current chain: ' + str(current_chain))
        surrounding_atoms = list()
        remaining_bonds = set()
        for bond in bonds.copy():
            current_atom = current_chain[-1]
            if current_atom in bond.atoms:
                atoms_copy = bond.atoms.copy()
                atoms_copy.remove(current_atom)
                other_atom = atoms_copy.pop()
                surrounding_atoms.append(other_atom)
            else:
                remaining_bonds.add(bond)
        if surrounding_atoms:
            finished_chains = list()
            for atom in surrounding_atoms:
                chain_copy = current_chain.copy()
                chain_copy.append(atom)
                finished_chains.extend(recursive(chain_copy, remaining_bonds))
        else:
            finished_chains = [current_chain]
        return finished_chains

    non_h_atoms = [atom for atom in self['atoms'] if atom['symbol'] != 'H']
    non_h_bonds = remove_unused_bonds(non_h_atoms, self['bonds'].copy())

    all_chains = list()
    for atom in non_h_atoms:
        chain = [atom]
        result = recursive(chain, non_h_bonds.copy())
        all_chains.extend(result)
        print(result)

    longest_chains = list()
    longest_chain_len = 0
    longest_carbon_chains = list()
    longest_carbon_chain_len = 0
    for chain in all_chains:
        if len(chain) == longest_chain_len:
            longest_chains.append(chain)
        if len(chain) > longest_chain_len:
            longest_chains = [chain]
            longest_chain_len = len(chain)
        if chain[0]['symbol'] == 'C' and chain[-1]['symbol'] == 'C':
            if len(chain) == longest_carbon_chain_len:
                longest_carbon_chains.append(chain)
            if len(chain) > longest_carbon_chain_len:
                longest_carbon_chains = [chain]
                longest_carbon_chain_len = len(chain)

    # todo: find best longest chain

    if longest_carbon_chains:
        return longest_carbon_chains
    else:
        return longest_chains


def _get_rings(self):
    def remove_unused_bonds(atoms, bonds):
        new_bonds = set()
        for bond in bonds:
            do_not_add = False
            for atom in bond.atoms:
                if atom not in atoms:
                    do_not_add = True
                    break
            if not do_not_add:
                new_bonds.add(bond)
        return new_bonds

    def remove_end_atoms(atoms, bonds):
        new_atoms = set()
        nr_removed_atoms = 0
        for atom in atoms:
            bond_count = 0
            for bond in bonds:
                if atom in bond.atoms:
                    bond_count += 1
            if bond_count >= 2:
                new_atoms.add(atom)
            else:
                nr_removed_atoms += 1
        return new_atoms, nr_removed_atoms

    def recursive(current_chain, bonds):
        surrounding_atoms = list()
        for bond in bonds:
            current_atom = current_chain[-1]
            if current_atom in bond.atoms:
                atoms_copy = bond.atoms.copy()
                atoms_copy.remove(current_atom)
                other_atom = atoms_copy.pop()
                if other_atom not in current_chain:
                    surrounding_atoms.append(other_atom)
        if chain[0] in surrounding_atoms:
            finished_rings = [chain]
        elif not surrounding_atoms:
            finished_rings = []
        else:
            finished_rings = list()
            for atom in surrounding_atoms:
                chain_copy = current_chain.copy()
                chain_copy.append(atom)
                finished_rings.extend(recursive(chain_copy, bonds))
        return finished_rings

    # remove all atoms and bonds that are not part of a ring:
    cyclic_atoms = [atom for atom in self['atoms'] if atom['symbol'] != 'H']
    cyclic_bonds = remove_unused_bonds(cyclic_atoms, self['bonds'].copy())
    while True:
        cyclic_atoms, nr_removed = remove_end_atoms(cyclic_atoms, cyclic_bonds)
        cyclic_bonds = remove_unused_bonds(cyclic_atoms, cyclic_bonds)
        if nr_removed == 0:
            break

    # find all possible rings:
    all_rings = list()
    for atom in cyclic_atoms:
        chain = [atom]
        all_rings.extend(recursive(chain, cyclic_bonds.copy()))

    # filter only unique rings out:
    unique_ring_sets = list()
    unique_rings = list()
    for ring in all_rings:
        ring_set = set()
        for atom in ring:
            ring_set.add(atom)
        new_ring = True
        for unique_ring_set in unique_ring_sets:
            if ring_set == unique_ring_set:
                new_ring = False
                break
        if new_ring:
            unique_ring_sets.append(ring_set)
            unique_rings.append(ring)
    return unique_rings
