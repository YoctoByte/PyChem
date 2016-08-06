from atoms import Atom

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
        examples for IUPAC: 'aluminium sulfate', 'carbon dioxide'
        examples for CAS: '10043-01-3', '124-38-9'
        """
        if data_type.lower() == 'formula':
            self.atoms, self.bonds = from_formula(molecule_data)
        elif data_type.lower() == 'smiles':
            self.atoms, self.bonds = from_smiles(molecule_data)
        elif data_type.lower() == 'iupac':
            self.atoms, self.bonds = from_iupac(molecule_data)
        elif data_type.lower() == 'cas':
            self.atoms, self.bonds = from_cas(molecule_data)
        elif data_type.lower() == 'name':
            self.atoms, self.bonds = from_name(molecule_data)
        else:
            self.atoms, self.bonds = from_data(molecule_data)


def from_formula(formula_string):
    return [], []


def from_iupac(iupac_string):
    return [], []


def from_smiles(smiles_string):
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
            molecule.add(new_atom)
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
            new_molecule = from_smiles(token[1:-1])
        elif token[0] == '[':
            token = token[1:-1]
            if token[1].isalpha():
                element = token[0:2]
                token = token[2:]
            else:
                element = token[0:1]
                token = token[1:]
            if token[0] in ['+', '-']:
                if token[1].isnumeric():
                    charge = int(token[1])
                    if token[0] == '-':
                        charge *= -1
                    token = token[2:]
                else:
                    charge = 1
                    if token[0] == '-':
                        charge *= -1
                    token = token[1:]
            chirality = None
            charge = None

    return fill_hydrogen(molecule)


def from_cas(cas_string):
    return [], []


def from_name(name):
    return [], []


def from_data(data):
    def guess_data_type(data):
        pass

    return [], []

from_smiles('COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C')
# '[Cu+2].[O-]S(=O)(=O)[O-]')
# CC(=O)C
# Molecule(formula='NaCO3')
# 'CH3COOH'
