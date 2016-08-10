from molecule.atoms import Atom
from molecule import iupac, smiles, cas
from molecule import gui

# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Bond:
    def __init__(self, type='', atoms=set(), energy=None, length=None):
        self.type = type
        self.atoms = atoms  # todo: self.atoms = set(atoms)
        self.energy = energy
        self.length = length


class Molecule:
    def __init__(self, molecule_data, data_type=None):
        """
        :param molecule_data: The molecule data (see examples)
        :param data_type: The molecule data type (see examples)
        examples for formula: 'Al2(SO4)3', 'CO2'
        examples for smiles: [Al+3].[O-]S(=O)(=O)[O-]O-C-O
        examples for name (iupac conventions): 'aluminium sulfate', 'carbon dioxide'
        examples for CAS: '10043-01-3', '124-38-9'
        """
        self.atoms = set()
        self.bonds = set()
        self.rings = None
        self.parent_chain = None
        self.iupac_name = None
        self.cas_number = None
        self.smiles = None
        self.formula = None
        if data_type.lower() == 'formula':
            self._from_formula(molecule_data)
            self.formula = molecule_data
        elif data_type.lower() == 'smiles':
            smiles.parse_from(self, molecule_data)
            self.smiles = molecule_data
        elif data_type.lower() == 'cas':
            cas.parse_from(self, molecule_data)
            self.cas_number = molecule_data
        elif data_type.lower() == 'iupac':
            cas.parse_from(self, molecule_data)
            self.iupac_name = molecule_data
        else:
            self._from_data(molecule_data)
        self.check_molecule()

    # todo:
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
        pass

    # todo:
    def _from_data(self, data):
        pass
