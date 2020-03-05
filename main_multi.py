from common.constants import *
from multi import thread_func as tf
import random
import rapidjson
from multiprocessing import Process, Queue, freeze_support
import os
from common.models import experiment_model as emodel
import time
"""
Every Neurons and Synapses are called as their index (or ID)
"""
MODEL = emodel.dopa_test_1

TICKS = MODEL.ticks
LOG_TICKS = MODEL.log_ticks

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
        self.ext_choices = None

        self.n_list = MODEL.n_model(**MODEL.n_kwargs)
        self.s_list = MODEL.s_model(**MODEL.s_kwargs)
        print('neuron : ',len(self.n_list))
        print('synapse :',len(self.s_list))
        self.synapse_connector()

        for i in range(MODEL.N_N_THREAD) :
            self.n_pre_Q.append(Queue())
            self.n_post_Q.append(Queue())
            self.n_potential_Q.append(Queue())
            self.n_procs.append(Process(
                target = tf.neuron_init,
                args = (
                    self.n_list[i*MODEL.N_NEURON:(i+1)*MODEL.N_NEURON],
                    self.n_pre_Q[i],
                    self.n_post_Q[i],
                    self.n_potential_Q[i],
                    i,
                    TICKS - LOG_TICKS,
                )
            ))
        for i in range(MODEL.N_S_THREAD) :
            self.s_pre_Q.append(Queue())
            self.s_post_Q.append(Queue())
            self.s_potential_Q.append(Queue())
            self.s_procs.append(Process(
                target = tf.synapse_init,
                args = (
                    self.s_list[i*MODEL.N_SYNAPSE : (i+1)*MODEL.N_SYNAPSE],
                    self.s_pre_Q[i],
                    self.s_post_Q[i],
                    self.s_potential_Q[i],
                    i,
                    TICKS - LOG_TICKS,
                )
            ))

    def synapse_connector(self) :
        for s in self.s_list :
            con = s.get_connection()
            idx = s.get_id()
            for pre in con[0] :
                self.n_list[pre].connect_ex_one(idx)
            self.n_list[con[1]].connect_in_one(idx)

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
        init_time = time.time()
        for _ in range(MODEL.N_N_THREAD):
            total_potentials.append([])
        for _ in range(MODEL.N_S_THREAD) :
            total_pre.append([])
            total_post.append([])
        ####################################Tick#############
        for t in range(TICKS) :
            print('Tick : {}'.format(t+1))
            external = MODEL.ext_model(**MODEL.ext_kwargs)
            for n in external :
                total_potentials[n[1]//MODEL.N_NEURON].append(n)

            for idx, Q in enumerate(self.n_potential_Q) :
                Q.put(total_potentials[idx])

            for idx in range(MODEL.N_S_THREAD) :
                self.s_pre_Q[idx].put(total_pre[idx])
                self.s_post_Q[idx].put(total_post[idx])

            #--------------------------------------------
            for i in range(MODEL.N_N_THREAD):
                total_potentials[i] = []
            for i in range(MODEL.N_S_THREAD) :
                total_pre[i] = []
                total_post[i] = []

            for idx in range(MODEL.N_N_THREAD) :
                for pre in self.n_pre_Q[idx].get() :
                    total_pre[pre[-1]//MODEL.N_SYNAPSE].append(pre)
                for post in self.n_post_Q[idx].get() :
                    total_post[post[-1]//MODEL.N_SYNAPSE].append(post)
            for idx in range(MODEL.N_S_THREAD) :
                for n in self.s_potential_Q[idx].get() :
                    total_potentials[n[-1]//MODEL.N_NEURON].append(n)

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

        print('total time : {:.2f}'.format(time.time()-init_time))

if __name__ == '__main__' :
    freeze_support()
    Main_multi().run()