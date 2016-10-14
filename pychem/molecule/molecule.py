import codecs
import hashlib
import json

from pychem.molecule import graph


def _load_data():
    with open('../pychem/data/elements.json') as elements_data_file:
        data = json.loads(elements_data_file.read())

    to_element = dict()
    for element, element_data in data.items():
        to_element[element_data['z']] = element
        to_element[element_data['symbol']] = element
        to_element[element] = element

    return data, to_element


ELEMENTS_DATA, TRANSLATE_ELEMENT = _load_data()


class Atom(graph.Node):
    def __init__(self, element, molecule, isotope=None, charge=0, aromatic=None, isomer=None):
        graph.Node.__init__(self)

        self.adj_atoms = self.adj_nodes
        self.bonds = self.edges

        self.molecule = molecule

        try:
            self.element = TRANSLATE_ELEMENT[element.capitalize()]
            element_data = ELEMENTS_DATA[self.element]
        except KeyError:
            raise ValueError('"' + str(element) + '" is not a valid element.')

        self.isotope = isotope
        self.charge = charge
        self.aromatic = aromatic
        self.isomer = isomer

        self.symbol = element_data['symbol']
        self.atomic_number = element_data['z']
        self.atomic_weight = element_data['atomic weight']
        self.electronegativity = element_data['electronegativity']

    def fill_hydrogen(self):
        if self.symbol not in ['B', 'C', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I']:
            return

        valence = {'B': 3, 'C': 4, 'N': 5, 'O': 6, 'P': 5, 'S': 6, 'F': 7, 'Cl': 7, 'Br': 7, 'I': 7}
        h_to_add = 8 - valence[self.symbol] + self.charge
        for bond in self.bonds:
            h_to_add -= bond.electron_count
        if self.aromatic:
            h_to_add -= 1

        for _ in range(4 - abs(4 - h_to_add)):
            hydrogen = Atom('H', self.molecule)
            bond = Bond(self, hydrogen)
            self.molecule.add_atom(hydrogen)
            self.molecule.add_bond(bond)

    def adjacent_atoms(self):
        return self.adj_nodes

    def bonds(self):
        return self.edges


class Bond(graph.Edge):
    def __init__(self, atom1, atom2, bond_type='-'):
        """
        Supported bond types are; 'normal', 'double', 'triple', 'quadruple', and 'aromatic'.
        """
        graph.Edge.__init__(self, atom1, atom2)
        bond_electrons = {'-': 1, '=': 2, '#': 3, '$': 4, ':': 1}
        self.electron_count = bond_electrons[bond_type]
        self.bond_type = bond_type

    def atoms(self):
        return self.sink, self.source


class Molecule(graph.Graph):
    def __init__(self):
        graph.Graph.__init__(self, directed=False, weighted=False)

        self.atoms = self.nodes
        self.bonds = self.edges
        self.electrons = set()

        self.mass = 0
        self.charge = 0

    def __iter__(self):
        yield from (atom for atom in self.nodes)

    def yield_bonds(self):
        yield from (bond for bond in self.edges)

    def get_bonds(self):
        return set(self.yield_bonds())

    def yield_atoms(self):
        yield from (atom for atom in self.nodes)

    def get_atoms(self):
        return set(self.yield_atoms())

    def add_atom(self, atom):
        if not isinstance(atom, Atom):
            raise ValueError('"' + str(atom) + '" not of type Atom.')
        if atom not in self.nodes:
            self.mass += atom.atomic_weight
        self.add_node(atom)

    def add_bond(self, bond):
        if not isinstance(bond, Bond):
            raise ValueError('"' + str(bond) + '" not of type Bond.')
        self.add_edge(bond)

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
                hydrogen = Atom('H', self)
                self.add_atom(hydrogen)
                self.add_bond(atoms={atom, hydrogen})
