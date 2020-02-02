from multiprocessing import Queue
import rapidjson
from common.constants import *

def logger_init(n_log_Q : Queue, N_Thread : int,  s_log_Q : Queue, S_Thread : int,) :
    total_log = {
        MULTI_potent_log : [],
        MULTI_fired_neuron_log : [],
        MULTI_weight_log : [],
        MULTI_fired_synapse_log : [],
    }
    tick = 1
    while True :
        n_tick = []
        s_tick = []
        potent_tick = []
        f_n_tick = []
        weight_tick = []
        f_s_tick = []
        for _ in range(N_Thread) :
            n_tick.append(n_log_Q.get())

        for _ in range(S_Thread) :
            s_tick.append(s_log_Q.get())

        if MULTI_sentinel in n_tick :
            break

        for threadlog in n_tick :
            potent_tick.extend(threadlog[MULTI_potent_log])
            f_n_tick.extend(threadlog[MULTI_fired_neuron_log])
        for threadlog in s_tick :
            weight_tick.extend(threadlog[MULTI_weight_log])
            f_s_tick.extend(threadlog[MULTI_fired_synapse_log])

        total_log[MULTI_potent_log].append(potent_tick)
        total_log[MULTI_fired_neuron_log].append(f_n_tick)
        total_log[MULTI_weight_log].append(weight_tick)
        total_log[MULTI_fired_synapse_log].append(f_s_tick)
        print(s_tick, tick)
        tick += 1

    with open('log_multi.json','w') as logfile :
        rapidjson.dump(total_log, logfile)
    print('saved')