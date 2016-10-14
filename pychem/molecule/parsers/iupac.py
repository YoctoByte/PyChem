from pychem.molecule.molecule import Molecule

import json
import os


parent_dir = os.path.split(os.path.dirname(__file__))[0]
parent_parent_dir = os.path.split(parent_dir)[0]
DATA_DIR = parent_parent_dir + '/data/iupac/'

with open(DATA_DIR + 'carbon_prefixes.json') as jf:
    CARBON_PREFIXES = json.load(jf)


def parse_from(name_string):
    pass


def parse_to(bonds, atoms):
    parent_chain = _find_parent_chain(bonds, atoms)
    side_chains = _find_side_chains(bonds, atoms, parent_chain)


def _find_parent_chain(bonds, atoms):

    # todo: if cyclic...

    carbon_atoms = set()
    for atom in atoms:
        if atom['symbol'] == 'C':
            carbon_atoms.add(atom)
    carbon_bonds = geometrics.list_active_bonds(bonds, carbon_atoms)

    parent_chain_candidates = list()
    best_substituent_count = 0
    for carbon_chain in geometrics.list_longest_chains(carbon_bonds, carbon_atoms):
        substituent_count = 0
        for bond in bonds:
            for atom in bond.atoms:
                if atom['symbol'] != 'H' and atom in carbon_chain:
                    substituent_count += 1
        if substituent_count == best_substituent_count:
            pass
        else:
            parent_chain_candidates = [carbon_chain]
            best_substituent_count = substituent_count


def _find_side_chains(bonds, atoms, parent_chain):
    pass


def _load_data_files():
    pass
    # with open(DATA_DIR + 'carbon_prefixes2.json', 'w') as jf:
    #     json.dump(carbon_prefixes, jf, separators=(',', ':'), indent=2, sort_keys=True)


_load_data_files()
