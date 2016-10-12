from pychem.modules import graph
# from pychem.parsers import smiles, iupac, cas, formula
import json
import hashlib
import codecs


def _load_data():
    with open('../project/PyChem/elements.json') as elements_data_file:
        raw_data = json.loads(elements_data_file.read())

    data = dict()
    for i, entry in enumerate(raw_data):
        entry['atomic number'] = i+1
        data[entry['element']] = entry
        data[entry['element'].lower()] = entry
        data[entry['element name']] = entry
        data[entry['element name'].lower()] = entry
        data[entry['atomic number']] = entry
    return data


ELEMENTS_DATA = _load_data()


class Atom:
    def __init__(self, element, isotope=None, charge=None, aromatic=None, isomer=None):
        try:
            element_data = ELEMENTS_DATA[element]
        except IndexError:
            raise ValueError('"' + element + '" is not a valid element.')

        self.isotope = isotope
        self.charge = charge
        self.aromatic = aromatic
        self.isomer = isomer

        self.symbol = element_data['element']
        self.element = element_data['element name']
        self.atomic_number = element_data['atomic number']
        self.atomic_weight = element_data['atomic weight']
        self.group = element_data['group']
        self.period = element_data['period']
        self.electronegativity = element_data['electronegativity']

        self.adjacent_atoms = set()
        self.bonds = dict()


class Bond:
    def __init__(self, atom1, atom2, bond_type='normal'):
        """
        Supported bond types are; 'normal', 'double', 'triple', 'quadruple', and 'aromatic'.
        """
        self.atoms = (atom1, atom2)
        self.atom1, self.atom2 = atom1, atom2
        self.bond_type = bond_type


class Molecule:
    def __init__(self, smiles=None):
        self._graph = graph.Graph(directed=False, weighted=False)
        self.mass = 0
        self.charge = 0

        if smiles:
            _parse_from_smiles(self, smiles)

        self.atom_priority_list = self._atom_priority_list()
        for atom in self:
            atom.calculate_isomere_stuff(self.atom_priority_list)

    def __iter__(self):
        for atom in self._graph:
            yield atom

    def add_atom(self, atom):
        added = self._graph.add_node(atom)
        if added:
            self.mass += atom.atomic_weight

    def add_bond(self, bond):
        self._graph.add_edge(bond.atom1, bond.atom2, identifier=bond)

    def _atom_priority_list(self):
        atom_priority_list = list()

        # Calculate distance order per atom:
        distance_order = dict()
        for atom in self:
            distance = 0
            distance_order[atom] = {distance: {atom}}
            used_atoms = {atom}
            while True:
                next_atoms = set()
                for other_atom in distance_order[atom][distance]:
                    for adjacent_atom in other_atom.adjacent_atoms:
                        if adjacent_atom not in used_atoms:
                            next_atoms.add(adjacent_atom)
                            used_atoms.add(adjacent_atom)
                distance += 1
                distance_order[atom][distance] = next_atoms
                if not next_atoms:
                    break

        # Initiate atom_priority_list:
        for atom in self:
            atom_priority_list.append([atom, -atom.atomic_number, atom.charge or 0])

        # Build the rest of atom_priority_list:
        distance = 1
        while True:
            go_to_next_iteration = False
            for item in atom_priority_list:
                atom = item[0]
                distance_score = 0
                if distance in distance_order[atom]:
                    go_to_next_iteration = True
                    for other_atom in distance_order[atom][distance]:
                        distance_score -= other_atom.atomic_number
                item.append(distance_score)
            if not go_to_next_iteration:
                break
            distance += 1

        # Order the list and return only the atoms:
        for i in reversed(range(1, distance+3)):
            atom_priority_list.sort(key=lambda x: x[i])
        only_atoms = list()
        for item in atom_priority_list:
            only_atoms.append(item[0])
        return only_atoms

    def bond_table(self, include_bonds=True):
        bond_table = list()

        atom_priority_list = self.atom_priority_list

        atom_numbering = dict()
        atom_to_string = dict()
        for atom in atom_priority_list:
            atom_to_string[atom] = atom.symbol
            if atom.symbol not in atom_numbering:
                atom_numbering[atom.symbol] = 0
            atom_numbering[atom.symbol] += 1
            atom_to_string[atom] += str(atom_numbering[atom.symbol])

        for atom in atom_priority_list:
            # sort the other_atom variable based on priority:
            adjacent_atoms = atom.bonds
            other_atoms = list()
            for other_atom in atom_priority_list:
                if other_atom in adjacent_atoms:
                    other_atoms.append(other_atom)

            for other_atom in other_atoms:
                bond_string = ''
                if include_bonds:
                    bond_type = atom.bonds[other_atom]
                    bond_string = ',' + bond_type
                entry = (atom_to_string[atom] + ',' + atom_to_string[other_atom] + bond_string + '\n')
                other_entry = (atom_to_string[other_atom] + ',' + atom_to_string[atom] + bond_string + '\n')
                if other_entry not in bond_table:
                    bond_table.append(entry)
        return ''.join(bond_table)

    def hash_molecule(self):
        md5 = hashlib.md5()
        md5.update(self.bond_table(include_bonds=False).encode('utf-8'))
        return codecs.encode(md5.digest(), 'hex')

    def hash_isomer(self):
        md5 = hashlib.md5()
        non_hashed_string = self.bond_table(include_bonds=False)

        charges = ''
        chiralities = ''
        for atom in self.atom_priority_list:
            charges += str(atom.charge)

        non_hashed_string += charges + chiralities
        md5.update(non_hashed_string.encode('utf-8'))
        return codecs.encode(md5.digest(), 'hex')

    def _fill_hydrogen(self):
        bond_electrons = {'-': 1, '=': 2, '#': 3, '$': 4, ':': 1}

        for atom in self.atoms.copy():
            try:
                hydrogen_to_add = atom.hydrogen_count
            except AttributeError:
                hydrogen_to_add = 0
                if atom.symbol in ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I']:
                    bonded_electrons = 0
                    for bond in atom.bonds.values():
                        bonded_electrons += bond_electrons[bond]
                    if atom.aromatic:
                        bonded_electrons += 1
                    hydrogen_to_add = 18 - (atom.group + bonded_electrons)
                    if atom.charge:
                        hydrogen_to_add += atom.charge

            for _ in range(hydrogen_to_add):
                hydrogen = Atom('H')
                self.add_atom(hydrogen)
                self.add_bond(atoms={atom, hydrogen})


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
            new_atom = Atom(element, isotope=isotope, charge=charge, aromatic=element.islower())
            new_atom.h_count = h_count
            molecule.add_atom(new_atom)
            if active_atom:
                molecule.add_bond(atoms={active_atom, new_atom}, bond_type=bond_type)
            active_atom = new_atom
            bond_type = '-'
        elif token.lower() in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
            new_atom = Atom(token, aromatic=token.islower())
            molecule.add_atom(new_atom)
            if active_atom:
                molecule.add_bond(atoms={active_atom, new_atom}, bond_type=bond_type)
            active_atom = new_atom
            bond_type = '-'
        elif token[0] == '%':
            label = token[1:]
            if label not in labels:
                labels[label] = active_atom
            else:
                molecule.add_bond(atoms={active_atom, labels[label]}, bond_type=bond_type)
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
    h_count = None
    charge = None
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