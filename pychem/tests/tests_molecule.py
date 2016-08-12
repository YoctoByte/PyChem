import unittest
from pychem.molecules import molecule, smiles


class TestStringMethods(unittest.TestCase):
    def test_smiles(self):
        m = molecule.Molecule('C=CC(=O)O')
        self.assertEqual(len(m.atoms), 9)
        self.assertEqual(len(m.bonds), 8)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
