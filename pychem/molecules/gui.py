import tkinter as tk
from math import cos, sin, pi
from pychem.molecules import geometrics

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

    def draw_molecule(self, bonds, atoms):
        class GUIAtom:
            def __init__(self, atom, pos=(0, 0)):
                self.symbol = atom['symbol']
                self.atom_reference = atom
                self.position = pos

        def draw_bonds_and_atoms(gbonds, gatoms):
            for gatom in gatoms:
                self.canvas.create_text(gatom.position, text=gatom.symbol)
            for gbond in gbonds:
                if gbond['type'] == '-':
                    self.canvas.create_line(gbond['line'])

        gatoms = list()
        gbonds = list()
        pos = (25, 87)
        angle = 30
        longest_chain = geometrics.list_longest_chains(bonds, atoms)[0]
        for atom in longest_chain:
            x, y = pos
            x += BOND_LENGTH * cos(angle/180*pi)
            y += BOND_LENGTH * sin(angle/180*pi)
            pos = (x, y)
            if angle > 0:
                angle -= 60
            else:
                angle += 60
            gatom = GUIAtom(atom, pos)
            gatoms.append(gatom)
            if gatoms:
                gbonds.append({'line': (gatoms[-1].position[0], gatoms[-1].position[1], x, y), 'type': '-'})
        draw_bonds_and_atoms(gbonds, gatoms)
        self.mainloop()
        self.terminate = True


class Canvas3D:
    pass
