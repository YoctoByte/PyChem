from pychem.parsers import smiles, cas, iupac, formula
from pychem.modules import graph
from pychem import gui
import json
import os


# todo: calculate resonance structures
# todo: predict stability of molecule


current_directory = os.path.dirname(__file__)
parent_dir = os.path.split(current_directory)[0]
DATA_FILE = parent_dir + '/data/elements.json'
DATA = list()
number_lookup = dict()


class Atom:
    def __init__(self, element, charge=0, chirality=None, isotope=None, aromatic=False):
        """
        :param element: the atom number, name or symbol of the element.
        """
        self.number = get_element_number(element)
        self.chirality = chirality
        self.charge = charge
        self.aromatic = False
        self.isotope = isotope
        self.aromatic = aromatic
        self.bonds = set()
        self.surrounding_atoms = set()

    def __getitem__(self, item):
        if item == 'valence electrons':
            return self._get_valence_electrons()
        else:
            return DATA[self.number][translate_attribute(item)]

    def _get_valence_electrons(self):
        electron_config = self['configuration']
        orbitals = electron_config.split(' ')
        if orbitals[0][0] == '[':
            orbitals.pop(0)

        electron_count = 0
        contains_d = False
        for orbital in orbitals:
            if orbital[1] in 'sp':
                electron_count += int(orbital[2:])
            if orbital[1] in 'df':
                contains_d = True

        if electron_count in [1, 2] and contains_d:
            return -1
        else:
            return electron_count

    @staticmethod
    def get_element_number(element):
        if isinstance(element, int):
            if 1 <= element <= 118:
                return element
            else:
                raise ValueError('Atom number should be between 1 and 118.')
        elif isinstance(element, str):
            try:
                return number_lookup[element]
            except KeyError:
                raise ValueError('Element name "' + element + '" not found.')
        else:
            raise ValueError('element should be an atom number (int), or element name (str).')

    @staticmethod
    def translate_attribute(attribute):
        return attribute

    @staticmethod
    def get_info(element, attribute):
        """
        :param element: An atom number, element name, or list containing these. keyword "all" is also accepted.
        :param attribute: The attribute that is retrieved. Example: "weight" or "electronegativity"
        :return: The desired information about the atom(s). If a value is not known, None is returned
        """
        if element == 'all':
            element = list(range(1, 119))
        if isinstance(element, list):
            values = list()
            for item in element:
                values.append(DATA[get_element_number(item)][attribute])
            return values
        else:
            return DATA[get_element_number(element)][attribute]

    @staticmethod
    def load_data():
        with open(DATA_FILE) as json_file:
            global DATA
            DATA = json.load(json_file)
        for element in DATA:
            try:
                number_lookup[element['name']] = element['z']
                number_lookup[element['symbol']] = element['z']
                try:
                    number_lookup[element['symbol'].lower()] = element['z']
                except AttributeError:
                    pass
            except KeyError:
                print(element)
        number_lookup[None] = -1


BOND_TYPES = {'-': 'single',
              '=': 'double',
              '#': 'triple',
              '$': 'quadruple',
              ':': 'aromatic'}


class Bond(graph.Edge):
    def __init__(self, bond_type='-', atoms=set(), energy=None, length=None, electron_count=None):
        self.bond_type_symbol = bond_type
        try:
            self.bond_type = BOND_TYPES[bond_type]
        except KeyError:
            self.bond_type = None
        self.atoms = set(atoms)
        self.energy = energy
        self.length = length
        self.electron_count = electron_count


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