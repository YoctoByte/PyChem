
bond_types = {'-': 'single',
              '=': 'double',
              '#': 'triple',
              '$': 'quadruple',
              ':': 'aromatic'}


class Bond:
    def __init__(self, bond_type='-', atoms=set(), energy=None, length=None):
        self.bond_type = bond_type
        self.atoms = set(atoms)
        self.energy = energy
        self.length = length
        self.electron_count = 0
