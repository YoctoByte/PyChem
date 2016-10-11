

def add_bonds_to_atoms(bonds):
    for bond in bonds:
        for atom in bond.atoms:
            atom.bonds.add(bond)
            for other_atom in bond.atoms.copy():
                if other_atom != atom:
                    atom.surrounding_atoms.add(other_atom)


def yield_all_chains(atoms, max_length=100):
    def recursive(current_chain):
        yield current_chain
        if len(current_chain) >= max_length:
            return
        current_atom = current_chain[-1]
        for other_atom in current_atom.surrounding_atoms:
            if other_atom not in current_chain:
                new_chain = current_chain.copy()
                new_chain.append(other_atom)
                yield from recursive(new_chain)

    for atom in atoms:
        chain = [atom]
        yield from recursive(chain)


def list_all_chains(atoms, max_length=100):
    return list(yield_all_chains(atoms, max_length))


def yield_ending_atoms(atoms, exclude_hydrogen=True):
    for atom in atoms:
        if atom['symbol'] == 'H' and exclude_hydrogen:
            continue
        real_surrounding_count = 0
        for surrounding_atom in atom.surrounding_atoms:
            if surrounding_atom in atoms:
                real_surrounding_count += 1
            if exclude_hydrogen and atom['symbol'] == 'H':
                real_surrounding_count -= 1
        if real_surrounding_count == 1:
            yield atom


def list_ending_atoms(atoms, exclude_hydrogen=True):
    return list(yield_ending_atoms(atoms, exclude_hydrogen))


def list_longest_chains(atoms, exclude_hydrogen=True, max_length=100):
    def recursive(current_chain):
        if len(current_chain) > max_length:
            return
        current_atom = current_chain[-1]
        yielded = False
        for other_atom in current_atom.surrounding_atoms:
            if (not exclude_hydrogen or (other_atom not in hydrogen_atoms and exclude_hydrogen)) \
                    and other_atom not in current_chain:
                new_chain = current_chain.copy()
                new_chain.append(other_atom)
                yield from recursive(new_chain)
                yielded = True
        if not yielded:
            yield current_chain

    ending_atoms = list_ending_atoms(atoms, exclude_hydrogen)
    hydrogen_atoms = [atom for atom in atoms if atom['symbol'] == 'H']

    # find the longest chains, starting from the ending atoms:
    longest_chains = list()
    length_longest_chain = 0
    for atom in ending_atoms:
        chain = [atom]
        for long_chain in recursive(chain):
            if len(long_chain) == length_longest_chain:
                longest_chains.append(long_chain)
            elif len(long_chain) > length_longest_chain:
                longest_chains = [long_chain]
                length_longest_chain = len(long_chain)
    return longest_chains


def remove_side_chains(atoms):
    length_previous_atoms = 0
    current_atoms = atoms.copy()
    while length_previous_atoms != len(current_atoms):
        ending_atoms = list_ending_atoms(atoms)
        length_previous_atoms = len(current_atoms)
        for atom in ending_atoms:
            current_atoms.remove(atom)
    return current_atoms


def yield_all_rings(atoms, max_length):
    def recursive(current_chain):
        yielded = False
        if len(current_chain) >= 3:
            first_atom = current_chain[0]
            last_atom = current_chain[-1]
            if first_atom in last_atom.surrounding_atoms:
                yield current_chain
                yielded = True
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

    new_atoms = remove_side_chains(atoms)
    for atom in new_atoms:
        yield from recursive([atom])


def yield_unique_rings(atoms, max_length=10):
    unique_ring_sets = list()
    unique_rings = list()
    for ring in yield_all_rings(atoms, max_length):
        ring_set = set(ring)
        if ring_set not in unique_ring_sets:
            unique_ring_sets.append(ring_set)
            unique_rings.append(ring)
    return unique_rings


def list_unique_rings(atoms, max_length=10):
    return list(yield_unique_rings(atoms, max_length))


# def check_molecule(bonds, atoms):
#     #xtodo: verify whether a molecule is valid or not; octet rule and stuff...
#     pass

