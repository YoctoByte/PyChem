import tkinter as tk
from math import cos, sin, pi

WINDOW_MIN_HEIGHT = 480
WINDOW_MIN_WIDTH = 800

# colors:
BG_STANDARD = '#AFAFAF'
FG_STANDARD = '#303030'

BOND_LENGTH = 50  # in pixels


class Canvas(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.ready = False
        self.terminate = False

        self.min_height = WINDOW_MIN_HEIGHT
        self.min_width = WINDOW_MIN_WIDTH

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('PyChem')
        self['bg'] = BG_STANDARD
        self.update()
        self.canvas = tk.Canvas(self, width=900, height=200)
        self.canvas.pack()

    def draw_molecule(self, molecule):
        class GUIAtom():
            def __init__(self, atom, pos=(0, 0)):
                self.symbol = atom['symbol']
                self.atom_reference = atom
                self.position = pos

        def draw_atoms_and_bonds(gatoms, bonds):
            for gatom in gatoms:
                self.canvas.create_text(gatom.position, text=gatom.symbol)
            for bond in bonds:
                if bond['type'] == '':
                    self.canvas.create_line(bond['line'])
                elif bond['type'] == '=':
                    pass
                elif bond['type'] == '#':
                    pass
                elif bond['type'] == '$':
                    pass

        atoms = list()  # list of dicts
        bonds = list()  # list of dicts
        pos = (25, 87)
        angle = 30
        longest_chain = molecule['longest chain'][0]
        previous_atom = None
        for atom in longest_chain:
            x, y = pos
            x += BOND_LENGTH * cos(angle/180*pi)
            y += (BOND_LENGTH * sin(angle/180*pi))
            pos = (x, y)
            if angle > 0:
                angle -= 60
            else:
                angle += 60
            gatom = GUIAtom(atom, pos)
            atoms.append(gatom)
            if previous_atom:
                bonds.append({'line': (previous_atom.position[0], previous_atom.position[1], x, y), 'type': ''})
            previous_atom = gatom
        draw_atoms_and_bonds(atoms, bonds)
        self.mainloop()
        self.terminate = True
