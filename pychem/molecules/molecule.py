# from pychem.molecules.atom import Atom
from pychem.molecules import smiles, cas, gui, iupac, formula, geometrics


# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Molecule:
    def __init__(self, molecule_data=None, data_type=None):
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
                self._from_data(molecule_data)
            geometrics.check_molecule(self.bonds, self.atoms)

    def draw_2d(self):
        canvas = gui.Canvas()
        canvas.draw_molecule(self.bonds, self.atoms)

    # todo:
    def _from_data(self, data):
        pass
