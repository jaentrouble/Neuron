import random

g_var = None
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

def dopa_test_e_1(inpt_strt, inpt_next_strt, n, rwrd_limit, rwrd_strt, rwrd_next_strt, potential) :
    """
    hand over indices as python range would expect
    if more than rwrd_limit is same , than reward will be given too
    """
    global g_var
    if g_var == None :
        g_var = random.choices(range(inpt_strt, inpt_next_strt), k=n)
    g_var = g_var[1:]
    g_var.append(random.randrange(inpt_strt, inpt_next_strt))
    tmp = []
    r = 0
    for i in g_var :
        tmp.append([potential, i])
        if i in range(n) :
            r += 1
    if r > rwrd_limit :
        for i in range(rwrd_strt, rwrd_next_strt) :
            tmp.append([potential, i])
    return tmp