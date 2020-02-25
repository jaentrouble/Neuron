from common.ns_subclasses import *
import random
from common.constants import *
import itertools as it
from common import tools
import math
"""
functions to create synapse lists
return s_list with Synapse objects
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
    
def dopa_test_s_1 (inpt_n, combi_r, outpt, v_n, overlap, dopa, reward, gamma) :
    s_list = []
    idx = 0
    cmbi_start = inpt_n
    outpt_start = cmbi_start + tools.combi(inpt_n, combi_r)
    val_start = outpt_start + outpt
    relay_start = val_start + v_n
    gaba_start = relay_start + v_n
    dopa_start = gaba_start + v_n
    reward_start = dopa_start + dopa
    random.seed(RANDOM_SEED)
    # 1
    combi = list(it.combinations(range(inpt_n), combi_r))
    for post_idx, c in enumerate(combi, cmbi_start) :
        for pre_idx in c :
            s_list.append(S_Dopa_dependent(
                pre_idx,
                post_idx,
                SYNAPSE_excitatory,
                list(range(dopa_start, reward_start)),
                idx,
            ))
            idx += 1
    # 2
    for post_idx, chunk in enumerate(tools.split(list(range(cmbi_start, outpt_start)), outpt),outpt_start) :
        for pre_idx in chunk :
            s_list.append(Synapse(pre_idx, post_idx, SYNAPSE_excitatory, idx))
            idx += 1
    # 3
    for post_idx, chunk in enumerate(tools.split(list(range(cmbi_start, outpt_start)), v_n, overlap), val_start):
        for pre_idx in chunk :
            s_list.append(S_Dopa_dependent(
                pre_idx,
                post_idx,
                SYNAPSE_excitatory,
                list(range(dopa_start, reward_start)),
                idx,
            ))
            idx += 1
    # 4
    for pre_idx in range(val_start, relay_start) :
        for post_idx in range(dopa_start, reward_start) :
            s_list.append(S_Dopa_pre_only(
                pre_idx,
                post_idx,
                SYNAPSE_excitatory,
                list(range(dopa_start,reward_start)),
                idx,
                discount= gamma,
                init_weight= 0,
            ))
            idx += 1
    # 5
    for pre_idx in range(val_start,relay_start) :
        post_idx = pre_idx + relay_start - val_start
        s_list.append(S_relay(
            pre_idx,
            post_idx,
            SYNAPSE_excitatory,
            idx,
        ))
        idx += 1
    # 6
    for pre_idx in range(relay_start, gaba_start):
        post_idx = pre_idx + gaba_start - relay_start
        s_list.append(S_relay(
            pre_idx,
            post_idx,
            SYNAPSE_excitatory,
            idx,
        ))
        idx += 1

    # 7
    for pre_idx in range(gaba_start, dopa_start) :
        for post_idx in range(dopa_start, reward_start):
            s_list.append(S_Dopa_pre_only(
                pre_idx,
                post_idx,
                SYNAPSE_inhibitory,
                list(range(dopa_start,reward_start)),
                idx,
                init_weight= 0,
            ))
            idx += 1
    # 8
    for pre_idx in range(reward_start, reward_start+reward) :
        for post_idx in range(dopa_start, reward_start):
            s_list.append(S_non_decaying(
                pre_idx,
                post_idx,
                SYNAPSE_excitatory,
                idx,
            ))
            idx += 1
    return s_list