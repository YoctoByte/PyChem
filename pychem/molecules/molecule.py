from pychem.molecules.parsers import smiles, cas, iupac, formula
from pychem.molecules import gui


# todo: calculate resonance structures
# todo: predict stability of molecule


class Molecule:
    def __init__(self, molecule_data=None, data_type=None):
        """
        :param molecule_data: The molecule data (see examples)
        :param data_type: The molecule data type (see examples)
        """
        self.atoms = set()
        self.bonds = set()
        self.rings = None
        self.parent_chain = None
        self.iupac_name = None
        self.cas_number = None
        self.smiles = None
        self.formula = None
        if molecule_data is not None:
            if data_type:
                if data_type.lower() == 'formula':
                    self.bonds, self.atoms = formula.from_formula(molecule_data)
                    self.formula = molecule_data
                elif data_type.lower() == 'smiles':
                    self.bonds, self.atoms = smiles.parse_from(molecule_data)
                    self.smiles = molecule_data
                elif data_type.lower() == 'cas':
                    self.bonds, self.atoms = cas.parse_from(molecule_data)
                    self.cas_number = molecule_data
                elif data_type.lower() == 'iupac':
                    self.bonds, self.atoms = iupac.parse_from(molecule_data)
                    self.iupac_name = molecule_data
            else:
                # parse
                pass

    def __iter__(self):
        for atom in self.atoms:
            yield atom

    def add_atom(self, atom):
        self.atoms.add(atom)

    def add_bond(self, bond):
        self.bonds.add(bond)
        for atom in bond.atoms:
            self.atoms.add(atom)
            for other_atom in bond.atoms:
                if other_atom != atom:
                    atom.surrounding_atoms.add(other_atom)

    def remove_atom(self, atom):
        pass

    def remove_bond(self, bond):
        pass

    def copy(self):
        molecule_copy = Molecule()
        for var in vars(self):
            print(var)

    def deepcopy(self):
        pass

    def draw_2d(self):
        canvas = gui.Canvas()
        canvas.draw_molecule(self.bonds, self.atoms)

molecule = Molecule()
molecule.copy()