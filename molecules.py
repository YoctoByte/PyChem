from atoms import Atom
import gui

# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Bond:
    def __init__(self, type='', atoms=set(), energy=None, length=None):
        self.type = type
        self.atoms = atoms # todo: self.atoms = set(atoms)
        self.energy = energy
        self.length = length


class Molecule:
    def __init__(self, molecule_data, data_type=None):
        """
        :param molecule_data: The molecule data (see examples)
        :param data_type: The molecule data type (see examples)
        examples for formula: 'Al2(SO4)3', 'CO2'
        example for smiles: [Al+3].[O-]S(=O)(=O)[O-]O-C-O
        examples for name (iupac conventions): 'aluminium sulfate', 'carbon dioxide'
        examples for CAS: '10043-01-3', '124-38-9'
        """
        self.properties = dict()
        self['atoms'] = set()
        self['bonds'] = set()
        self['rings'] = None
        self['longest chain'] = None
        self['iupac name'] = None
        self['cas number'] = None
        self['smiles'] = None
        self['formula'] = None
        if data_type.lower() == 'formula':
            self._from_formula(molecule_data)
            self['formula'] = molecule_data
        elif data_type.lower() in ['smiles', 'smilesx']:
            self._from_smiles(molecule_data)
            self['smiles'] = molecule_data
        elif data_type.lower() == 'cas':
            self._from_cas(molecule_data)
            self['cas number'] = molecule_data
        elif data_type.lower() == 'name':
            self._from_name(molecule_data)
            self['iupac name'] = molecule_data
        else:
            self._from_data(molecule_data)
        if data_type != 'smilesx':
            self.check_molecule()

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __getitem__(self, item):
        if item == 'longest chain' and self.properties[item] is None:
            self[item] = self._find_longest_chain()
        elif item == 'rings' and self.properties[item] is None:
            self[item] = self._find_rings()
        elif item == 'smiles' and not self.properties[item]:
            self[item] = self._to_smiles()
        elif item == 'formula' and not self.properties[item]:
            self[item] = self._to_formula()
        return self.properties[item]

    def __str__(self):
        pass

    def draw_2d(self):
        canvas = gui.Canvas()
        canvas.draw_molecule(self)

    def check_molecule(self):
        # todo: verify whether a molecule is valid or not; octet rule and stuff...
        pass

    def _from_formula(self, formula_string):
        pass

    def _to_formula(self):
        return self['formula']

    def _from_smiles(self, smiles_string):
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

        def connect_bonds():
            labels = dict()
            new_bonds = set()
            bonds_to_remove = set()
            for bond in self['bonds']:
                for label in bond.atoms:
                    if isinstance(label, str):
                        atoms_copy = bond.atoms.copy()
                        atoms_copy.remove(label)
                        atom = atoms_copy.pop()
                        if label not in labels:
                            labels[label] = atom
                        else:
                            new_bonds.add(Bond(atoms={atom, labels[label]}))
                        bonds_to_remove.add(bond)
            self['bonds'].update(new_bonds)
            for bond in bonds_to_remove:
                self['bonds'].remove(bond)

        def fill_hydrogen():
            pass

        self.first_atom = None
        self.first_bond_type = ''
        active_atom = None
        bond_type = ''
        for token in tokenize(smiles_string):
            if token.lower() in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
                new_atom = Atom(token)
                if token in ['b', 'c', 'n', 'o', 'p', 's', 'f', 'cl', 'br', 'i']:
                    new_atom.aromatic = True
                if not self.first_atom:
                    self.first_atom = new_atom
                if active_atom:
                    self['bonds'].add(Bond(atoms={active_atom, new_atom}, type=bond_type))
                self['atoms'].add(new_atom)
                active_atom = new_atom
                bond_type = ''
            elif token in '0123456789':
                self['bonds'].add(Bond(atoms={active_atom, token}, type=bond_type))
                bond_type = ''
            elif token in ['=', '#', '$']:
                bond_type = token
                if not self.first_atom:
                    self.first_bond_type = token
            elif token[0] == '(':
                side_chain = Molecule(token[1:-1], 'smilesx')
                self['atoms'].update(side_chain['atoms'])
                self['bonds'].update(side_chain['bonds'])
                self['bonds'].add(Bond(atoms={active_atom, side_chain.first_atom}, type=side_chain.first_bond_type))
            elif token[0] == '[':
                token = token[1:-1]
                if token[1].isalpha():
                    element = token[0:2]
                    token = token[2:]
                else:
                    element = token[0:1]
                    token = token[1:]
                new_atom = Atom(element)
                if token[0] in ['+', '-']:
                    if token[1:].isnumeric():
                        charge = int(token[1])
                        if token[0] == '-':
                            charge *= -1
                        token = token[2:]
                    else:
                        charge = 1
                        if token[0] == '-':
                            charge *= -1
                        token = token[1:]
                    new_atom.charge = charge
                    chirality = None  # todo
                    if active_atom:
                        self['bonds'].add(Bond(atoms={active_atom, new_atom}, type=bond_type))
                    self['atoms'].add(new_atom)
                    active_atom = new_atom
                    bond_type = ''
        connect_bonds()
        fill_hydrogen()

    # todo:
    def _to_smiles(self):
        return self['smiles']

    # todo:
    def _from_cas(self, cas_string):
        pass

    # todo:
    def _to_cas(self):
        return self['cas number']

    # todo:
    def _from_name(self, name):
        pass

    # todo:
    def _to_name(self):
        return self['iupac name']

    # todo:
    def _from_data(self, data):
        def guess_data_type(data):
            if '[' in data:
                pass
                # not name or cas

    def _find_rings(self):
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


molecule = Molecule('O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5', 'smiles')
# for atom in molecule.atoms:
#     print(atom['name'])
# molecule.draw_2d()
for ring in molecule['rings']:
    print('returned chain: ', str(ring))
    # print(len(chain))


# C=CC(=O)O
# COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C
# O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5
# [Cu+2].[O-]S(=O)(=O)[O-]
# CC(=O)C
# Molecule(formula='NaCO3')
# CH3COOH = CC(=O)O
