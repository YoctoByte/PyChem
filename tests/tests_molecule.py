import unittest
from pychem import molecule


class TestSmiles(unittest.TestCase):
    def test_smiles(self):
        ethane = molecule.Molecule(smiles='CC')
        benzene = molecule.Molecule(smiles='c1ccccc1')
        benzene2 = molecule.Molecule(smiles='C1=CC=CC=C1')
        alanine = molecule.Molecule(smiles='O=C(O)C(N)C')
        asparagine = molecule.Molecule(smiles='O=C(N)C[C@H](N)C(=O)O')
        cephalostatin = molecule.Molecule(smiles='C[C@@](C)(O1)C[C@@H](O)[C@@]1(O2)[C@@H](C)[C@@H]3CC=C4[C@]3(C2)C(=O)C'
                                                 '[C@H]5[C@H]4CC[C@@H](C6)[C@]5(C)Cc(n7)c6nc(C[C@@]89(C))c7C[C@@H]8CC[C'
                                                 '@@H]%10[C@@H]9C[C@@H](O)[C@@]%11(C)C%10=C[C@H](O%12)[C@]%11(O)[C@H](C'
                                                 ')[C@]%12(O%13)[C@H](O)C[C@@]%13(C)CO')
        for mol, nr_of_atoms in [(ethane, 8),
                                 # (benzene, 12),
                                 (benzene2, 12),
                                 (alanine, 13),
                                 (asparagine, 17),
                                 (cephalostatin, 140)
                                 ]:
            print('-----')
            for atom in mol.atoms:
                print(atom.symbol, len(atom.adj_atoms))
            self.assertEqual(len(mol.atoms), nr_of_atoms)

if __name__ == '__main__':
    unittest.main()
