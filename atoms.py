import json


DATA_FILE = 'files/elements.json'
DATA = list()
number_lookup = dict()


class Atom:
    def __init__(self, element):
        """
        :param element: the atom number, name or symbol of the element.
        """
        self.number = get_element_number(element)
        self.surroundings = list()

    def __getitem__(self, item):
        return DATA[self.number][translate_attribute(item)]


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
    if isinstance(element, list):
        values = list()
        for item in element:
            values.append(DATA[get_element_number(item)][attribute])
        return values
    elif element == 'all':
        values = list()
        for item in range(1, 119):
            values.append(DATA[get_element_number(item)][attribute])
        return values
    else:
        return DATA[get_element_number(element)][attribute]


def load_data():
    with open(DATA_FILE) as json_file:
        global DATA
        DATA = json.load(json_file)
    for element in DATA:
        number_lookup[element['name']] = element['z']
        number_lookup[element['symbol']] = element['z']
    number_lookup[None] = -1


load_data()
