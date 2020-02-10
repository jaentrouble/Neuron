from multiprocessing import Queue
from common.constants import *
import rapidjson
import os

def neuron_init(n_list : list, pre_Q : Queue, post_Q : Queue, Potential_Q : Queue, num : int, log_max = -1):
    potent_log = [] # [[id, potential],...]
    fired_log = [] # [id,...]
    start_index = n_list[0].get_id()
    while True :
        fired_to_neurons = Potential_Q.get()
        pre_fired = []
        post_fired = []
        if fired_to_neurons == MULTI_sentinel :
            # Log_q.put({
            #     MULTI_potent_log : potent_log,
            #     MULTI_fired_neuron_log : fired_log,
            # })
            break
        for n in n_list :
            n.tick()
        # 4
        for n in fired_to_neurons :
            n_list[n[1]-start_index].input_potential(n[0])

        # 1
        tmp_potent = []
        tmp_fired = []
        for idx, n in enumerate(n_list, start = start_index) :
            tmp_potent.append([idx, n.get_potential()])
            if n.is_fired() :
                i, e = n.get_signal()
                pre_fired.extend(e)
                post_fired.extend(i)
                tmp_fired.append(idx)
        
        if log_max > 0  and len(potent_log) >= log_max:
            potent_log.pop(0)
            fired_log.pop(0)
            potent_log.append(tmp_potent)
            fired_log.append(tmp_fired)
        else :
            potent_log.append(tmp_potent)
            fired_log.append(tmp_fired)
        pre_Q.put(pre_fired)
        post_Q.put(post_fired)

    with open(os.path.join(LOG_path, LOG_multi_neuron_name.format(num)), 'w') as logfile :
        rapidjson.dump({
            str(MULTI_potent_log) : potent_log,
            str(MULTI_fired_neuron_log) : fired_log,
        }, logfile)

def synapse_init(s_list : list, pre_Q : Queue, post_Q : Queue, Potential_Q : Queue, num : int, log_max = -1) :
    weight_log = []
    fired_log = []
    start_index = s_list[0].get_id()
    while True :
        pre_fired = pre_Q.get()
        post_fired = post_Q.get()
        if pre_fired == MULTI_sentinel or post_fired == MULTI_sentinel :
            # Log_q.put({
            #     MULTI_weight_log : weight_log,
            #     MULTI_fired_synapse_log : fired_log,
            # })
            break
        fired_to_neurons = []
        for s in s_list :
            s.tick()

        # 2
        for s in post_fired :
            s_list[s[1] - start_index].post_fired(s[0])
        for s in pre_fired :
            s_list[s[1] - start_index].pre_fired(s[0])

        # 3
        tmp_weight = []
        tmp_fired = []
        for idx, s in enumerate(s_list, start = start_index) :
            tmp_weight.append([idx, s.get_weight()])
            if s.is_fired():
                fired_to_neurons.append(s.get_signal())
                tmp_fired.append(idx)
        if log_max > 0 and len(weight_log) >= log_max :
            weight_log.pop(0)
            fired_log.pop(0)
            weight_log.append(tmp_weight)
            fired_log.append(tmp_fired)
        else :
            weight_log.append(tmp_weight)
            fired_log.append(tmp_fired)
        Potential_Q.put(fired_to_neurons)

    with open(os.path.join(LOG_path, LOG_multi_synapse_name.format(num)), 'w') as logfile :
        rapidjson.dump({
            str(MULTI_weight_log) : weight_log,
            str(MULTI_fired_synapse_log) : fired_log,
        }, logfile)
# if __name__ == '__main__' :
#     freeze_support()