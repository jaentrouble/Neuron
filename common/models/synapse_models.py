from common.neuron import Neuron, Synapse
import random
from common.constants import *
"""
functions to create synapse lists

"""

def random_synapses(S_num : int,N_num : int ,ex_percent : float):
    s_list = []
    for idx in range(S_num) :
        pre = random.randrange(0, N_num)
        post = random.randrange(0, N_num)
        if random.random() < ex_percent :
            s_list.append(Synapse(pre, post, SYNAPSE_excitatory, idx))
        else :
            s_list.append(Synapse(pre, post, SYNAPSE_inhibitory, idx))

    return s_list