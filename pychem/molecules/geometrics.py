

def find_all_chains(bonds, atoms):
    def recursive(current_chain, all_bonds):
        yield current_chain
        current_atom = current_chain[-1]
        for bond in all_bonds.copy():
            if current_atom in bond.atoms:
                atoms_copy = bond.atoms.copy()
                atoms_copy.remove(current_atom)
                other_atom = atoms_copy.pop()
                if other_atom not in current_chain:
                    chain_copy = current_chain.copy()
                    chain_copy.append(other_atom)
                    yield from recursive(chain_copy, all_bonds)

    for atom in atoms:
        chain = [atom]
        yield from recursive(chain, bonds)


def _remove_unused_bonds(bonds, atoms):
    new_bonds = set()
    for bond in bonds:
        do_not_add = False
        for atom in bond.atoms:
            if atom not in atoms:
                do_not_add = True
                break
        if not do_not_add:
            new_bonds.add(bond)
    return new_bonds


def find_longest_chains(bonds, atoms):
    non_h_atoms = [atom for atom in atoms if atom['symbol'] != 'H']
    non_h_bonds = _remove_unused_bonds(bonds.copy(), non_h_atoms)

    longest_chains = list()
    longest_chain_len = 0
    for chain in find_all_chains(non_h_bonds, non_h_atoms):
        if len(chain) == longest_chain_len:
            longest_chains.append(chain)
        if len(chain) > longest_chain_len:
            longest_chains = [chain]
            longest_chain_len = len(chain)
    return longest_chains


def _find_all_rings(bonds, atoms):
    for chain in find_all_chains(bonds, atoms):
        if len(chain) < 3:
            continue
        first_atom = chain[0]
        last_atom = chain[-1]
        for bond in bonds:
            if first_atom in bond.atoms and last_atom in bond.atoms:
                yield chain
                break


def find_rings(bonds, atoms):
    unique_ring_sets = list()
    unique_rings = list()
    for ring in _find_all_rings(bonds, atoms):
        ring_set = set(ring)
        if ring_set not in unique_ring_sets:
            unique_ring_sets.append(ring_set)
            unique_rings.append(ring)
    return unique_rings
