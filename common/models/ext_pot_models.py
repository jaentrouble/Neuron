import random

g_var = None
g_var2 = None
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
    global g_var, g_var2
    if g_var == None :
        g_var = random.choices(range(inpt_strt, inpt_next_strt), k=n)
    if g_var2 == None :
        g_var2 = 0
    if g_var2 % 8 == 0 :
        g_var = g_var[1:]
        lft = list(range(inpt_strt, inpt_next_strt))
        lft = [l for l in lft if not (l in g_var)]
        g_var.append(random.choice(lft))
    tmp = []
    r = 0
    for i in g_var :
        tmp.append([potential, i])
        if i in range(n) :
            r += 1
    if r > rwrd_limit :
        for i in range(rwrd_strt, rwrd_next_strt) :
            tmp.append([potential, i])
    g_var2 += 1
    return tmp