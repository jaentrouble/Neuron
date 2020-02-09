import random

g_var = None
g_var2 = None
g_var3 = None
"""
functions to create external potential inputs
return list of external potentials [[potential, index], ...]
"""

def random_fixed_n_potentials(n, n_num, potential) :
    """
    input 'potential' to n random neurons
    these n neurons are fixed
    """
    global g_var, g_var2
    if g_var == None:
        random.seed(0)
        g_var = random.choices(range(n_num), k= n + 5)
        g_var2 = True
    tmp = []
    if g_var2 :
        pick = g_var[:n-2]
        pick.extend(random.choices(g_var[n-2:], k=2))
        for i in pick :
            tmp.append([potential, i])
        g_var2 = not g_var2
    else :
        g_var2 = not g_var2
    return tmp

def dopa_test_e_1(inpt_strt, inpt_next_strt, n, rwrd_limit, rwrd_strt, rwrd_next_strt, potential) :
    """
    hand over indices as python range would expect
    if more than rwrd_limit is same , than reward will be given too
    """
    global g_var, g_var2, g_var3
    if g_var == None :
        # g_var = random.choices(range(inpt_strt, inpt_next_strt), k=n)
        g_var = list(range(inpt_next_strt-n, inpt_next_strt))
    if g_var2 == None :
        g_var2 = 0
    if not(g_var2 % 50) :
        g_var = g_var[1:]
        # lft = list(range(inpt_strt, inpt_next_strt))
        # lft = [l for l in lft if not (l in g_var)]
        # g_var.append(random.choice(lft))
        g_var.append((g_var[-1]+1-inpt_strt)%(inpt_next_strt-inpt_strt) + inpt_strt)
    tmp = []
    r = 0
    if not(g_var2 % 4):
        if g_var3 :
            for i in range(rwrd_strt, rwrd_next_strt) :
                tmp.append([potential, i])
            g_var3 = False
        for i in g_var :
            tmp.append([potential, i])
            if i in range(n) :
                r += 1
        if r > rwrd_limit :
            g_var3 = True
    g_var2 += 1
    return tmp