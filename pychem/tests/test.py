# from pychem.molecules import molecule
from pychem.molecules import smiles, gui


bonds, atoms = smiles.parse_from('CCc(c1)ccc2[n+]1ccc3c2Nc4c3cccc4')
all_rings = smiles.find_rings(bonds, atoms)
for chain in all_rings:
    print(len(chain))
print('total nr rings found: ' + str(len(all_rings)))
# canvas = gui.Canvas()
# canvas.draw_molecule(bonds, atoms)
# for atom in atoms:
#     print(atom, atom['name'])
# for bond in bonds:
#     print(bond.atoms)


# O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5
# C=CC(=O)O
# C1CCCCC1
# c1ccccc1
# COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C
# OC[C@@H](O1)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)1
# [Cu+2].[O-]S(=O)(=O)[O-]      copper sulfate
# O=Cc1ccc(O)c(OC)c1    vanillin
