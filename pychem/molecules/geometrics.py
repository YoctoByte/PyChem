

def _yield_surrounding_atoms(bonds, atom):
    for bond in bonds:
        if atom in bond.atoms:
            atoms_copy = bond.atoms.copy()
            atoms_copy.remove(atom)
            while atoms_copy:
                other_atom = atoms_copy.pop()
                yield other_atom


def _list_surrounding_atoms(bonds, atom):
    return list(_yield_surrounding_atoms(bonds, atom))


def _simplify(bonds, atoms):
    """
    bug: does not work for full cyclic molecules
    :param bonds:
    :param atoms:
    :return:
    """
    inter_atoms = set()
    joint_atoms = set()
    bond_count = dict()
    for atom in atoms.copy():
        nr_of_bonds = len(_list_surrounding_atoms(bonds, atom))
        bond_count[atom] = nr_of_bonds
        if nr_of_bonds != 2:
            joint_atoms.add(atom)
        else:
            inter_atoms.add(atom)

    simplified_bonds = set()
    for atom in joint_atoms:
        for surrounding_atom in bond_count[atom]:
            chain = [atom, surrounding_atom]
            previous_atom = atom
            current_atom = surrounding_atom
            while bond_count[surrounding_atom] == 2:
                surrounding_atoms = _list_surrounding_atoms(bonds, current_atom)
                surrounding_atoms.remove(previous_atom)
                previous_atom = current_atom
                current_atom = surrounding_atoms.pop()
                chain.append(current_atom)
            simplified_bonds.add(chain)

    return simplified_bonds, joint_atoms


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


def list_all_chains(bonds, atoms, max_length=100):
    return list(yield_all_chains(bonds, atoms, max_length))


def yield_ending_atoms(bonds, atoms):
    for atom in atoms.copy():
        bond_count = 0
        for bond in bonds:
            if atom in bond.atoms:
                bond_count += 1
        if bond_count == 1:
            yield atom


def list_ending_atoms(bonds, atoms):
    return list(yield_ending_atoms(bonds, atoms))


def list_longest_chains(bonds, atoms, exclude_hydrogen=True, max_length=100):
    length_longest_chain = 0

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

    if exclude_hydrogen:
        non_h_atoms = [atom for atom in atoms if atom['symbol'] != 'H']
        remaining_bonds = list_active_bonds(bonds.copy(), non_h_atoms)
        ending_atoms = list_ending_atoms(remaining_bonds, non_h_atoms)
    else:
        remaining_bonds = bonds
        ending_atoms = list_ending_atoms(bonds, atoms)

    # find the longest chains, starting from the ending atoms:
    longest_chains = list()
    length_longest_chain = 0
    for atom in ending_atoms:
        chain = [atom]
        for chain in recursive(chain, remaining_bonds):
            if len(chain) == length_longest_chain:
                longest_chains.append(chain)
            elif len(chain) > length_longest_chain:
                longest_chains = [chain]
                length_longest_chain = len(chain)
    return longest_chains


def yield_active_bonds(bonds, atoms):
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


def list_active_bonds(bonds, atoms):
    return list(yield_active_bonds(bonds, atoms))


def _remove_side_chains(bonds, atoms):
    previous_atoms = set()
    current_bonds = bonds
    current_atoms = atoms
    while previous_atoms != current_atoms:
        current_bonds = list_active_bonds(current_bonds, current_atoms)
        current_atoms = list_ending_atoms(bonds, atoms)
    return list_active_bonds(current_bonds, current_atoms), current_atoms


def yield_all_rings(bonds, atoms, max_length):
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
    for ring in yield_all_rings(bonds, atoms, max_length):
        ring_set = set(ring)
        if ring_set not in unique_ring_sets:
            unique_ring_sets.append(ring_set)
            unique_rings.append(ring)
    return unique_rings


# def check_molecule(bonds, atoms):
#     #xtodo: verify whether a molecule is valid or not; octet rule and stuff...
#     pass


def _bonds_to_atoms(bonds):
    new_atoms = set()
    for bond in bonds:
        for atom in bond.atoms:
            new_atoms.add(atom)
    return new_atoms
