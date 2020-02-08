from common.constants import *
from common.ns_subclasses import *
from common import tools
"""
functions to create synapse lists
return n_list with Neuron objects
"""

def simple_neurons(N_num : int) :
    n_list = []
    for idx in range(N_num) :
        n_list.append(Neuron(idx))
    return n_list

def dopa_test_n_1(inpt_n, combi_r, outpt, v_n, dopa, reward) :
    n_list = []
    idx = 0
    gaba = v_n
    for _ in range(inpt_n) :
        n_list.append(Neuron(idx))
        idx += 1
    for _ in range(tools.combi(inpt_n, combi_r)):
        n_list.append(Neuron(idx))
        idx += 1
    for _ in range(outpt + v_n + gaba) :
        n_list.append(Neuron(idx))
        idx += 1
    for _ in range(dopa) :
        n_list.append(N_Dopa_emit(idx))
        idx += 1
    for _ in range(reward) :
        n_list.append(Neuron(idx))
        idx += 1
    return n_list