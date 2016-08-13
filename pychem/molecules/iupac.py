import json
import os

parent_dir = os.path.split(os.path.dirname(__file__))[0]
DATA_DIR = parent_dir + '/data/iupac/'

CARBON_PREFIXES = None


def parse_from(molecule, name_string):
    pass


def parse_to(molecule):
    parent_chain = _find_parent_chain(molecule)
    side_chains = _find_side_chains(molecule, parent_chain)


def _find_parent_chain(molecule):
    # find all longest carbon chains
    # 1. It should have the maximum number of substituents of the suffix functional group. By suffix, it
    # is meant that the parent functional group should have a suffix, unlike halogen substituents. If
    # more than one functional group is present, the one with highest precedence should be used.
    # 2. It should have the maximum number of multiple bonds
    # 3. It should have the maximum number of single bonds.
    # 4. It should have the maximum length.
    pass


def _find_side_chains(molecule, parent_chain):
    pass


def _load_carbon_prefixes():
    with open(DATA_DIR + 'carbon_prefixes.json') as jf:
        carbon_prefixes = json.load(jf)
    for _, prefix in carbon_prefixes.items():
        print(prefix)
    with open(DATA_DIR + 'carbon_prefixes2.json', 'w') as jf:
        json.dump(carbon_prefixes, jf, separators=(',', ':'), indent=2, sort_keys=True)


_load_carbon_prefixes()
