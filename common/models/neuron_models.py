from common.constants import *
from common.neuron import Neuron
"""
functions to create synapse lists
return n_list with Neuron objects
"""


def simple_neurons(N_num : int) :
    n_list = []
    for idx in range(N_num) :
        n_list.append(Neuron(idx))
    return n_list