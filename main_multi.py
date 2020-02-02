from common import neuron
from common.constants import *
from multi import thread_func as tf
import random
import rapidjson
from multiprocessing import Process, Queue, freeze_support
import os
"""
Every Neurons and Synapses are called as their index (or ID)
"""
#Numbers of Threads to (N)eurons and (S)ynapses
N_N_THREAD = 1
N_S_THREAD = 4
# numbers per Thread
N_NEURON = 100
N_SYNAPSE = 300
# Excitatory synapse ratio
S_E_ratio = 1
# Total simulation time
TICKS = 1000
# N of neurons to give External input
EXTERNAL_N_neuron = 10
EXTERNAL_potential = 20

class Main_multi() :
    def __init__ (self) :
        self.n_procs = []
        self.s_procs = []
        self.n_pre_Q = []
        self.n_post_Q = []
        self.n_potential_Q = []
        self.s_pre_Q = []
        self.s_post_Q = []
        self.s_potential_Q = []
        self.n_log_Q = Queue()
        self.s_log_Q = Queue()
        self.n_list = []
        self.s_list = []
        self.ext_choices = None

        for i in range(N_N_THREAD * N_NEURON) :
            self.n_list.append(neuron.Neuron(i))

        for i in range(N_S_THREAD * N_SYNAPSE) :
            self.s_list.append(self.synapse_maker(i, self.n_list))

        for i in range(N_N_THREAD) :
            self.n_pre_Q.append(Queue())
            self.n_post_Q.append(Queue())
            self.n_potential_Q.append(Queue())
            self.n_procs.append(Process(
                target = tf.neuron_init,
                args = (
                    self.n_list[i*N_NEURON:(i+1)*N_NEURON],
                    self.n_pre_Q[i],
                    self.n_post_Q[i],
                    self.n_potential_Q[i],
                    i,
                )
            ))
        for i in range(N_S_THREAD) :
            self.s_pre_Q.append(Queue())
            self.s_post_Q.append(Queue())
            self.s_potential_Q.append(Queue())
            self.s_procs.append(Process(
                target = tf.synapse_init,
                args = (
                    self.s_list[i*N_SYNAPSE : (i+1)*N_SYNAPSE],
                    self.s_pre_Q[i],
                    self.s_post_Q[i],
                    self.s_potential_Q[i],
                    i,
                )
            ))
    def synapse_maker(self, idx, n_list : list) :
        pre = random.randrange(0,len(n_list))
        post = random.randrange(0,len(n_list))
        n_list[pre].connect_ex_one(idx)
        n_list[post].connect_in_one(idx)
        if random.random() < S_E_ratio :
            return neuron.Synapse(pre, post, SYNAPSE_excitatory, idx)
        else :
            return neuron.Synapse(pre, post, SYNAPSE_inhibitory, idx)

    def external_potential(self, n, potential) :
        """
        external_potential
        n : potential list from 0 to n-1 neuron
        potential : potential to give to the neurons
        """
        if self.ext_choices == None :
            self.ext_choices = random.choices(range(len(self.n_list)), k=n)
        tmp = []
        for i in self.ext_choices :
            tmp.append([potential,i])
        return tmp

    def connection_logging(self) :
        """
        connection_logging
        synapse-based
        [[0's pre, 0's post], [1's pre, 1's post], ... ]
        """
        connections = []
        for s in self.s_list :
            connections.append(s.get_connection())
        with open(os.path.join(LOG_path, LOG_connection_name), 'w') as logfile :
            rapidjson.dump(connections, logfile)


    def run(self) :
        for n_p in self.n_procs :
            n_p.start()
        for s_p in self.s_procs :
            s_p.start()
        total_potentials = []
        total_pre = []
        total_post = []
        for _ in range(N_N_THREAD):
            total_potentials.append([])
        for _ in range(N_S_THREAD) :
            total_pre.append([])
            total_post.append([])
        ####################################Tick#############
        for t in range(TICKS) :
            print('Tick : {}'.format(t+1))
            external = self.external_potential(EXTERNAL_N_neuron, EXTERNAL_potential)
            for n in external :
                total_potentials[n[1]//N_NEURON].append(n)

            for idx, Q in enumerate(self.n_potential_Q) :
                Q.put(total_potentials[idx])

            for idx in range(N_S_THREAD) :
                self.s_pre_Q[idx].put(total_pre[idx])
                self.s_post_Q[idx].put(total_post[idx])

            #--------------------------------------------
            for i in range(N_N_THREAD):
                total_potentials[i] = []
            for i in range(N_S_THREAD) :
                total_pre[i] = []
                total_post[i] = []

            for idx in range(N_N_THREAD) :
                for pre in self.n_pre_Q[idx].get() :
                    total_pre[pre//N_SYNAPSE].append(pre)
                for post in self.n_post_Q[idx].get() :
                    total_post[post//N_SYNAPSE].append(post)
            for idx in range(N_S_THREAD) :
                for n in self.s_potential_Q[idx].get() :
                    total_potentials[n[1]//N_NEURON].append(n)

        #########################################################
        for Q in self.n_potential_Q :
            Q.put(MULTI_sentinel)
        for Q in self.s_post_Q :
            Q.put(MULTI_sentinel)
        for Q in self.s_pre_Q :
            Q.put(MULTI_sentinel)
        # neuron_log = []
        # synapse_log = []
        # while len(neuron_log) < N_N_THREAD :
        #     neuron_log.append(self.n_log_Q.get())
        # while len(synapse_log) < N_S_THREAD :
        #     synapse_log.append(self.s_log_Q.get())
        self.connection_logging()

        for n_p in self.n_procs :
            n_p.join()
        for s_p in self.s_procs :
            s_p.join()

if __name__ == '__main__' :
    freeze_support()
    Main_multi().run()