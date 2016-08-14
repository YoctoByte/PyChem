# from pychem.molecules import molecule
from pychem.molecules import smiles, gui, geometrics


bonds, atoms = smiles.parse_from('C[C@@](C)(O1)C[C@@H](O)[C@@]1(O2)[C@@H](C)[C@@H]3CC=C4[C@]3(C2)C(=O)C[C@H]5[C@H]4CC[C@@H](C6)[C@]5(C)Cc(n7)c6nc(C[C@@]89(C))c7C[C@@H]8CC[C@@H]%10[C@@H]9C[C@@H](O)[C@@]%11(C)C%10=C[C@H](O%12)[C@]%11(O)[C@H](C)[C@]%12(O%13)[C@H](O)C[C@@]%13(C)CO')
print('molecule parsed')
all_rings = geometrics.find_rings(bonds, atoms)
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
