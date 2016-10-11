import unittest
from pychem import molecule
from pychem.parsers import smiles


class TestStringMethods(unittest.TestCase):
    def test_smiles(self):
        m = molecule.Molecule('C=CC(=O)O')
        self.assertEqual(len(m.atoms), 9)
        self.assertEqual(len(m.bonds), 8)


if __name__ == '__main__':
    unittest.main()
