import rapidjson
from common.constants import *
import os

class Log() :
    def __init__(self, n_log_names : list, s_log_names : list, c_log_name : str):
        potent = []
        fired_neuron = []
        weight = []
        fired_synapse = []
        for nl in n_log_names :
            with open(os.path.join(LOG_path, nl), 'r') as logfile :
                tmp = rapidjson.load(logfile)
                potent.append(tmp[str(MULTI_potent_log)])
                fired_neuron.append(tmp[str(MULTI_fired_neuron_log)])
        for sl in s_log_names :
            with open(os.path.join(LOG_path, sl), 'r') as logfile :
                tmp = rapidjson.load(logfile)
                weight.append(tmp[str(MULTI_weight_log)])
                fired_synapse.append(tmp[str(MULTI_fired_synapse_log)])

        with open(os.path.join(LOG_path, c_log_name)) as logfile :
            self.connections = rapidjson.load(logfile)

        self.merged_potent = []
        for t in range(len(potent[0])) :
            tick = []
            for thread in potent :
                tick.extend(thread[t])
            self.merged_potent.append(tick)

        self.merged_f_n = []
        for t in range(len(fired_neuron[0])) :
            tick = []
            for thread in fired_neuron :
                tick.extend(thread[t])
            self.merged_f_n.append(tick)

        self.merged_weight = []
        for t in range(len(weight[0])) :
            tick = []
            for thread in weight :
                tick.extend(thread[t])
            self.merged_weight.append(tick)

        self.merged_f_s = []
        for t in range(len(fired_synapse[0])) :
            tick = []
            for thread in fired_synapse :
                tick.extend(thread[t])
            self.merged_f_s.append(tick)

        self.n_num = len(self.merged_potent[0])
        self.s_num = len(self.connections)
        self.max_tick = len(self.merged_potent)

    def get_total_pot_log(self) :
        return self.merged_potent.copy()
    
    def get_total_wt_log(self) :
        return self.merged_weight.copy()

    def get_log(self, tick : int) :
        """
        get_log
        get a dictionary of a certain tick
        returns {
            MULTI_potent_log : self.merged_potent[tick],
            MULTI_fired_neuron_log : self.merged_f_n[tick],
            MULTI_weight_log : self.merged_weight[tick],
            MULTI_fired_synapse_log : self.merged_f_s[tick],
        }
        """
        return {
            MULTI_potent_log : self.merged_potent[tick],
            MULTI_fired_neuron_log : self.merged_f_n[tick],
            MULTI_weight_log : self.merged_weight[tick],
            MULTI_fired_synapse_log : self.merged_f_s[tick],
        }

    def get_connections(self) :
        return self.connections.copy()

    def get_n_num(self):
        return self.n_num

    def get_s_num(self) :
        return self.s_num

    def get_max_tick(self) :
        return self.max_tick-1