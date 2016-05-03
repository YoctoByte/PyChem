from fileparser import parse_from_string


DATA_FILE = 'files/elements.txt'


class Atom:
    # todo: singleton for performance
    def __init__(self, atom):
        self.data = list()
        self.read_data()
        self.atom_nr = self.get_atom_nr(atom)
        self.elem_data = self.data[self.atom_nr]

    def __getitem__(self, item):
        return self.elem_data[item]

    def get_atom_nr(self, atom):
        for element in self.data:
            if atom in [element['sym'], element['element']]:
                return element['z']
        return -1

    def read_data(self):
        with open(DATA_FILE, 'r') as file:
            for line in file:
                self.data.append(parse_from_string(line))
            file.close()


def stuff():
    new_elements = list()
    with open('files/elements.txt') as file:
        for line in file:
            new_element = dict()
            element = parse_from_string(line)
            for key in element:
                if key in ['Origin of name']:
                    continue
                if key in ['Melt', 'Boil', 'Heat', 'Neg', 'Abundance', 'Density', 'Atomic weight', 'Period', 'Group']:
                    if type(element[key]) not in [int, float] and element[key] is not None:
                        print(element['Element'] + ': ' + key + ' = ' + str(element[key]))
                new_element[key.lower()] = element[key]
            new_elements.append(new_element)
        file.close()

    with open('files/new_elements', 'w') as file:
        for element in new_elements:
            file.write(str(element) + '\n')
        file.close()
