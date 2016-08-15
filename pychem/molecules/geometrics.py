

def yield_all_chains(bonds, atoms, max_length=100):
    def recursive(current_chain, all_bonds):
        yield current_chain
        if len(current_chain) >= max_length:
            return
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
    for chain in yield_all_chains(non_h_bonds, non_h_atoms):
        if len(chain) == longest_chain_len:
            longest_chains.append(chain)
        if len(chain) > longest_chain_len:
            longest_chains = [chain]
            longest_chain_len = len(chain)
    return longest_chains


def _remove_side_chains(bonds, atoms):
    new_atoms = atoms.copy()
    nr_removed_atoms = -1
    while nr_removed_atoms != 0:
        bonds = _remove_unused_bonds(bonds, new_atoms)
        nr_removed_atoms = 0
        for atom in new_atoms.copy():
            bond_count = 0
            for bond in bonds:
                if atom in bond.atoms:
                    bond_count += 1
            if bond_count >= 2:
                new_atoms.add(atom)
            else:
                nr_removed_atoms += 1
                new_atoms.remove(atom)
    return _remove_unused_bonds(bonds, new_atoms), new_atoms


def _find_all_rings(bonds, atoms, max_length):
    def recursive(current_chain, all_bonds):
        yielded = False
        if len(current_chain) >= 3:
            first_atom = current_chain[0]
            last_atom = current_chain[-1]
            for bond in all_bonds:
                if first_atom in bond.atoms and last_atom in bond.atoms:
                    yield current_chain
                    yielded = True
                    break
        if len(current_chain) < max_length and not yielded:
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

    new_bonds, new_atoms = _remove_side_chains(bonds, atoms)
    for atom in new_atoms:
        yield from recursive([atom], new_bonds)


def find_rings(bonds, atoms, max_length=10):
    unique_ring_sets = list()
    unique_rings = list()
    for ring in _find_all_rings(bonds, atoms, max_length):
        ring_set = set(ring)
        if ring_set not in unique_ring_sets:
            unique_ring_sets.append(ring_set)
            unique_rings.append(ring)
    return unique_rings
