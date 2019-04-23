# -*- coding: utf-8 -*-
"""
PURPOSE:
    Tools for ZND detonation simulation and chemical sensitivity analysis using
    cantera

CREATED BY:
    Mick Carter
    Oregon State University
    CIRE and Propulsion Lab
    cartemic@oregonstate.edu
"""

import cantera as ct


def _enforce_species_list(species):
    if isinstance(species, str):
        species = [species.upper()]
    elif hasattr(species, '__iter__'):
        species = [s.upper() for s in species]
    else:
        raise TypeError('Bad species type: %s' % type(species))

    return species


# noinspection PyArgumentList
def solution_with_inerts(
        mech,
        inert_species
):
    inert_species = _enforce_species_list(inert_species)
    species = ct.Species.listFromFile(mech)
    reactions = []
    for rxn in ct.Reaction.listFromFile(mech):
        if not any([
            s in list(rxn.reactants) + list(rxn.products)
            for s in inert_species
        ]):
            reactions.append(rxn)

    return ct.Solution(
        thermo='IdealGas',
        species=species,
        reactions=reactions
    )


def single_reaction_sensitivity(
        gas,
        idx_rxn,
        f,
        dk_i=1e-2
):
    """
    Calculates the normalized sensitivity of some function f the ith reaction:

                            s_i = (k_i / f) / (df / dk_i)                    (1)

    using the following steps:
        1. Calculate f
        2. Log values of f and k_i
        3. Perturb reaction i by the value p (i.e. the arrhenius constant A
           becomes (1+dk_i)*A
        4. Recalculate f
        5. Calculate df
        6. Calculate and return the normalized sensitivity coefficient, s_i

    Parameters
    ----------
    gas
    idx_rxn
    f
    dk_i

    Returns
    -------

    """
    pass


if __name__ == '__main__':
    mechanism = 'gri30.cti'

    rxns = ct.Reaction.listFromFile(mechanism)
    print(len([rxn for rxn in rxns if 'O' not in list(rxn.reactants) + list(rxn.products) and 'O2' not in list(rxn.reactants) + list(rxn.products)]))
    print(len(ct.Species.listFromFile(mechanism)))

    test_gas = solution_with_inerts('gri30.cti', ['o', 'o2'])
    print(test_gas.n_reactions, test_gas.n_species)
