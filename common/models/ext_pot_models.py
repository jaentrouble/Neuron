import random

"""
functions to create external potential inputs
return list of external potentials [[potential, index], ...]
"""

def random_fixed_n_potentials(n, n_num, potential) :
    """
    input 'potential' to n random neurons
    these n neurons are fixed
    """
    random.seed(0)
    ext_choices = random.choices(range(n_num), k=n)
    tmp = []
    for i in ext_choices :
        tmp.append([potential, i])
    return tmp