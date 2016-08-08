from atoms import Atom
import gui

# todo: verify whether a molecule is valid or not; octet rule and stuff...
# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


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
        self.atoms = set()
        self.bonds = list()
        if data_type.lower() == 'formula':
            self.from_formula(molecule_data)
        elif data_type.lower() in ['smiles', 'smilesx']:
            self.from_smiles(molecule_data)
        elif data_type.lower() == 'cas':
            self.from_cas(molecule_data)
        elif data_type.lower() == 'name':
            self.from_name(molecule_data)
        else:
            self.from_data(molecule_data)
        if data_type != 'smilesx':
            self.check_molecule()

    def __str__(self):
        pass

    def draw_2d(self):
        canvas = gui.Canvas()
        canvas.draw_molecule(self)

    def check_molecule(self):
        pass

    def from_formula(self, formula_string):
        pass

    def from_smiles(self, smiles_string):
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
            pass

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
                    self.bonds.append({'atoms': {active_atom, new_atom}, 'type': bond_type})
                self.atoms.add(new_atom)
                active_atom = new_atom
                bond_type = ''
            elif isinstance(token, int):
                self.bonds.append({'atoms': {active_atom, token}, 'type': bond_type})
                bond_type = ''
            elif token in ['=', '#', '$']:
                bond_type = token
                if not self.first_atom:
                    self.first_bond_type = token
            elif token[0] == '(':
                side_chain = Molecule(token[1:-1], 'smilesx')
                self.atoms.update(side_chain.atoms)
                self.bonds.extend(side_chain.bonds)
                self.bonds.append({'atoms': {active_atom, side_chain.first_atom}, 'type': side_chain.first_bond_type})
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
                        self.bonds.append({'atoms': {active_atom, new_atom}, 'type': bond_type})
                    self.atoms.add(new_atom)
                    active_atom = new_atom
                    bond_type = ''

    def from_cas(self, cas_string):
        pass

    def from_name(self, name):
        pass

    def from_data(self, data):
        def guess_data_type(data):
            if '[' in data:
                pass
                # not name or cas

    def longest_chain(self):
        def remove_bonds(atoms, bonds):
            new_bonds = list()
            for bond in bonds:
                do_not_add = False
                for atom in bond['atoms']:
                    if atom not in atoms:
                        do_not_add = True
                        break
                if not do_not_add:
                    new_bonds.append(bond)
            return new_bonds

        def recursive(chain, bonds):
            other_atoms = list()
            new_bonds = list()
            for bond in bonds.copy():
                last_atom = chain[-1]
                if last_atom in bond['atoms']:
                    bond_copy = bond.copy()
                    atoms_copy = bond_copy['atoms'].copy()
                    atoms_copy.remove(last_atom)
                    other_atom = atoms_copy.pop()
                    other_atoms.append(other_atom)
                else:
                    new_bonds.append(bond)
            if other_atoms:
                new_chains = list()
                for atom in other_atoms:
                    new_chain = chain.copy()
                    new_chain.append(atom)
                    new_chains.extend(recursive(new_chain, new_bonds))
            else:
                new_chains = [chain]
            return new_chains

        non_h_atoms = [atom for atom in self.atoms if atom['symbol'] != 'H']
        non_h_bonds = remove_bonds(non_h_atoms, self.bonds.copy())

        all_chains = list()
        for atom in non_h_atoms:
            chain = [atom]
            atoms_copy = self.atoms.copy()
            atoms_copy.remove(atom)
            result = recursive(chain, non_h_bonds.copy())
            all_chains.extend(result)
            print('result: ' + str(result))
            print('all_chains:')
            for chain in all_chains:
                print('    ' + str(chain))

        longest_chains = list()
        longest_chain_len = 0
        for chain in all_chains:
            if len(chain) == longest_chain_len:
                longest_chains.append(chain)
            if len(chain) > longest_chain_len:
                longest_chains = [chain]
                longest_chain_len = len(chain)

        # todo: find best longest chain

        return longest_chains


molecule = Molecule('C=CC(=O)O', 'smiles')
# for atom in molecule.atoms:
#     print(atom['name'])
# molecule.draw_2d()
for chain in molecule.longest_chain():
    print('returned chain: ', str(chain))
    # print(len(chain))

# C=CC(=O)O
# COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C
# O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5
# [Cu+2].[O-]S(=O)(=O)[O-]
# CC(=O)C
# Molecule(formula='NaCO3')
# CH3COOH = CC(=O)O
