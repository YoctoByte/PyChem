import json
import os


current_directory = os.path.dirname(__file__)
parent_dir = os.path.split(current_directory)[0]
DATA_FILE = parent_dir + '/data/elements.json'
DATA = list()
number_lookup = dict()


class Atom:
    def __init__(self, element, charge=0, chirality=None):
        """
        :param element: the atom number, name or symbol of the element.
        """
        self.number = get_element_number(element)
        self.chirality = chirality
        self.charge = charge
        self.aromatic = False

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


def translate_attribute(attribute):
    return attribute


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


load_data()
