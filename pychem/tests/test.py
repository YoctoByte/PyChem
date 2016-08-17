from pychem.molecules.parsers import smiles, iupac
from pychem.molecules import gui, geometrics


oenanthotoxin = 'CCC[C@@H](O)CC\C=C\C=C\C#CC#C\C=C\CO'
pyrethrin = 'COC(=O)C(\C)=C\C1C(C)(C)[C@H]1C(=O)O[C@@H]2C(C)=C(C(=O)C2)CC=CC=C'
aflatoxin = 'O1C=C[C@H]([C@H]1O2)c3c2cc(OC)c4c3OC(=O)C5=C4CCC(=O)5'
glucose = 'OC[C@@H](O1)[C@@H](O)[C@H](O)[C@@H](O)[C@@H](O)1'
bergenin = 'OC[C@@H](O1)[C@@H](O)[C@H](O)[C@@H]2[C@@H]1c3c(O)c(OC)c(O)cc3C(=O)O2'
random_pheromone = 'CC(=O)OCCC(/C)=C\C[C@H](C(C)=C)CCC=C'
flavopereirin = 'CCc(c1)ccc2[n+]1ccc3c2Nc4c3cccc4'
copper_sulfate = '[Cu+2].[O-]S(=O)(=O)[O-]'
vanillin = 'O=Cc1ccc(O)c(OC)c1'
pyrazine_rex = 'C[C@@](C)(O1)C[C@@H](O)[C@@]1(O2)[C@@H](C)[C@@H]3CC=C4[C@]3(C2)C(=O)C[C@H]5[C@H]4CC[C@@H](C6)[C@]5(C' \
               ')Cc(n7)c6nc(C[C@@]89(C))c7C[C@@H]8CC[C@@H]%10[C@@H]9C[C@@H](O)[C@@]%11(C)C%10=C[C@H](O%12)[C@]%11(O)' \
               '[C@H](C)[C@]%12(O%13)[C@H](O)C[C@@]%13(C)CO'


def test_find_rings():
    bonds, atoms = smiles.parse_from(pyrazine_rex)
    print('molecule parsed')
    all_rings = geometrics.find_rings(bonds, atoms, max_length=6)
    for chain in all_rings:
        print(len(chain))
    print('total nr rings found: ' + str(len(all_rings)))


def test_find_longest_chains():
    atoms = smiles.parse_from(pyrazine_rex)
    for chain in geometrics.list_longest_chains(atoms):
        print(len(chain))
        for atom in chain:
            print(atom['name'])


def test_find_parent_chain():
    bonds, atoms = smiles.parse_from(glucose)
    parent_chains = iupac._find_parent_chain(bonds, atoms)
    for atom in parent_chains[0]:
        print(atom['name'])


def draw_2d():
    bonds, atoms = smiles.parse_from(glucose)
    canvas = gui.Canvas()
    canvas.draw_molecule(bonds, atoms)

test_find_longest_chains()
