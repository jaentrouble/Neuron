from multiprocessing import Queue, Barrier
from common.constants import *
import rapidjson
import os
import tqdm
import numpy as np
import math

def neuron_init(n_list : list, pre_Q_list : list, post_Q_list : list, Potential_Q_list : list,
                barrier : Barrier, N_SYNAPSE : int, num : int, ticks : int, log_begin = -1,):
    potent_log = [] # [[id, potential],...]
    fired_log = [] # [id,...]
    start_index = n_list[0].get_id()
    N_S_THREAD = len(pre_Q_list)
    pre_fired = [[] for _ in range(N_S_THREAD)]
    post_fired = [[] for _ in range(N_S_THREAD)]
    if num < N_S_THREAD :
        put_order = np.arange(num, num+ N_S_THREAD)%N_S_THREAD
        get_order = np.arange(num + N_S_THREAD, num, -1)%N_S_THREAD
        # Don't forget to get external potentials
        get_order = np.append(get_order, -1)
    else :
        put_order = np.arange(N_S_THREAD)
        get_order = np.arange(N_S_THREAD-1, -1, -1)
        # Don't forget to get external potentials
        get_order = np.append(get_order, -1)
    
    for count in range(ticks) :
        # Put to synapse thread Queues
        for idx in put_order :
            pre_Q_list[idx].put(pre_fired[idx])
            post_Q_list[idx].put(post_fired[idx])
        # Wait until synapse threads gets all items
        barrier.wait()
        # Get all from neuron's Queues and start calculation
        fired_to_neurons = []
        for idx in get_order :
            fired_to_neurons.extend(Potential_Q_list[idx].get())
        pre_fired = [[] for _ in range(N_S_THREAD)]
        post_fired = [[] for _ in range(N_S_THREAD)]
        # if fired_to_neurons == MULTI_sentinel :
            # Log_q.put({
            #     MULTI_potent_log : potent_log,
            #     MULTI_fired_neuron_log : fired_log,
            # })
            # break
        for n in n_list :
            n.tick()
        # 4
        for n in fired_to_neurons :
            n_list[n[-1]-start_index].input_potential(n[0])

        # 1
        tmp_potent = []
        tmp_fired = []
        for idx, n in enumerate(n_list, start = start_index) :
            if count >= log_begin :
                p = n.get_potential()
                if not p :
                    tmp_potent.append([idx, 0])
                else :
                    tmp_potent.append([idx, int(p*100+0.5)/100])
            if n.is_fired() :
                i, e = n.get_signal()
                for pre in e :
                    pre_fired[pre[-1]//N_SYNAPSE].append(pre)
                for post in i :
                    post_fired[post[-1]//N_SYNAPSE].append(post)
                if count >= log_begin :
                    tmp_fired.append(idx)

        if count >= log_begin :
            potent_log.append(tmp_potent)
            fired_log.append(tmp_fired)

        # pre_Q.put(pre_fired)
        # post_Q.put(post_fired)

    with open(os.path.join(LOG_path, LOG_multi_neuron_name.format(num)), 'w') as logfile :
        rapidjson.dump({
            str(MULTI_potent_log) : potent_log,
            str(MULTI_fired_neuron_log) : fired_log
        }, logfile, number_mode= rapidjson.NM_NATIVE)

def synapse_init(s_list : list, pre_Q_list : list, post_Q_list : list, Potential_Q_list : list,
                 barrier : Barrier, N_NEURON : int, num : int, ticks : int, log_begin = -1) :
    weight_log = []
    fired_log = []
    start_index = s_list[0].get_id()
    N_N_THREAD = len(Potential_Q_list)
    fired_to_neurons = [[] for _ in range(N_N_THREAD)]
    if num < N_N_THREAD :
        put_order = np.arange(num, num+ N_N_THREAD)%N_N_THREAD
        get_order = np.arange(num + N_N_THREAD, num, -1)%N_N_THREAD
    else :
        put_order = np.arange(N_N_THREAD)
        get_order = np.arange(N_N_THREAD-1, -1, -1)

    for count in range(ticks) :
        pre_fired = []
        post_fired = []
        # Get from pre/post queue, sent by Neurons
        for idx in get_order:
            pre_fired.extend(pre_Q_list[idx].get())
            post_fired.extend(post_Q_list[idx].get())
        # Tell finished getting from queues
        barrier.wait()
        # Put items BEFORE calculation starts, i.e. putting the items from the past iter.
        for idx in put_order :
            Potential_Q_list[idx].put(fired_to_neurons[idx])
        if pre_fired == MULTI_sentinel or post_fired == MULTI_sentinel :
            # Log_q.put({
            #     MULTI_weight_log : weight_log,
            #     MULTI_fired_synapse_log : fired_log,
            # })
            break
        fired_to_neurons = [[] for _ in range(N_N_THREAD)]
        for s in s_list :
            s.tick()

        # 2
        for s in post_fired :
            s_list[s[-1] - start_index].post_fired(s)
        for s in pre_fired :
            s_list[s[-1] - start_index].pre_fired(s)

        # 3
        tmp_weight = []
        tmp_fired = []
        for idx, s in enumerate(s_list, start = start_index) :
            if count >= log_begin :
                w = s.get_weight()
                if not w :
                    tmp_weight.append([idx, 0])
                else :
                    tmp_weight.append([idx, int(w*100+0.5)/100])
            if s.is_fired():
                pot = s.get_signal()
                fired_to_neurons[pot[-1]//N_NEURON].append(pot)
                if count >= log_begin :
                    tmp_fired.append(idx)

        if count >= log_begin :
            weight_log.append(tmp_weight)
            fired_log.append(tmp_fired)

        # Potential_Q.put(fired_to_neurons)

    with open(os.path.join(LOG_path, LOG_multi_synapse_name.format(num)), 'w') as logfile :
        rapidjson.dump({
            str(MULTI_weight_log) : weight_log,
            str(MULTI_fired_synapse_log) : fired_log,
        }, logfile, number_mode=rapidjson.NM_NATIVE)
# if __name__ == '__main__' :
#     freeze_support()

def ext_pot_init(ext_model, ext_kwargs, Potential_Q_list : list, barrier : Barrier,
                 N_NEURON : int, ticks : int):
    N_N_THREAD = len(Potential_Q_list)
    for count in range(ticks) :
        total_potentials = [[] for _ in range(N_N_THREAD)]
        external = ext_model(**ext_kwargs)
        for n in external :
            total_potentials[n[-1]// N_NEURON].append(n)
        barrier.wait()
        for idx, ftn in enumerate(total_potentials) :
            Potential_Q_list[idx].put(ftn)

def s_to_n_distributer(n_pot_q : list, s_pot_q : list, N_N_THREAD : int,
                       N_NEURON : int, N_S_THREAD : int, ticks : int,
                       ext_model, ext_kwargs):
    total_potentials = []
    for _ in range(N_N_THREAD) :
        total_potentials.append([])
    for t in tqdm.trange(ticks, ncols = 150, mininterval = 1, unit = 'tick') :
        external = ext_model(**ext_kwargs)
        for n in external :
            total_potentials[n[-1]// N_NEURON].append(n)
        for idx, Q in enumerate(n_pot_q) :
            Q.put(total_potentials[idx])

        #----------------------------------------------------
        for i in range(N_N_THREAD) :
            total_potentials[i] = []

        for idx in range(N_S_THREAD) :
            for n in s_pot_q[idx].get() :
                total_potentials[n[-1]// N_NEURON].append(n)
        
    for Q in n_pot_q :
        Q.put(MULTI_sentinel)

def n_to_s_distributer(s_pre_Q : list, s_post_Q : list,
                       n_pre_Q : list, n_post_Q : list,
                       N_S_THREAD : int, N_SYNAPSE : int,
                       N_N_THREAD : int, ticks : int) :
    total_pre = []
    total_post = []
    for _ in range(N_S_THREAD) :
        total_pre.append([])
        total_post.append([])
    for t in range(ticks) :
        for idx in range(N_S_THREAD) :
            s_pre_Q[idx].put(total_pre[idx])
            s_post_Q[idx].put(total_post[idx])

        #-------------------------------------------
        for i in range(N_S_THREAD) :
            total_pre[i] = []
            total_post[i] = []

        for idx in range(N_N_THREAD) :
            for pre in n_pre_Q[idx].get() :
                total_pre[pre[-1] // N_SYNAPSE].append(pre)
            for post in n_post_Q[idx].get() :
                total_post[post[-1] // N_SYNAPSE].append(post)

    for Q in s_post_Q :
        Q.put(MULTI_sentinel)
    for Q in s_pre_Q :
        Q.put(MULTI_sentinel)