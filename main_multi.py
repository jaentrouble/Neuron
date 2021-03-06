from common.constants import *
from multi import thread_func as tf
import random
import rapidjson
from multiprocessing import Process, Queue, freeze_support, Barrier
import os
from common.models import experiment_model as emodel
import time
import tqdm
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
        # self.n_pre_Q = []
        # self.n_post_Q = []
        # self.n_potential_Q = []
        # self.s_pre_Q = []
        # self.s_post_Q = []
        # self.s_potential_Q = []
        # self.n_log_Q = Queue()
        # self.s_log_Q = Queue()
        # self.ext_choices = None

        self.n_list = MODEL.n_model(**MODEL.n_kwargs)
        self.s_list = MODEL.s_model(**MODEL.s_kwargs)
        print('neuron : ',len(self.n_list))
        print('synapse :',len(self.s_list))
        self.synapse_connector()

        # extra one for main thread and another one for external potential thread
        self.barrier = Barrier(
            MODEL.N_S_THREAD + MODEL.N_N_THREAD + 2
        )

        # pre_Q and post_Q belongs to synapses
        self.pre_Q = []
        for _ in range(MODEL.N_S_THREAD) :
            self.pre_Q.append([Queue() for _ in range(MODEL.N_N_THREAD)])
        self.post_Q = []
        for _ in range(MODEL.N_S_THREAD) :
            self.post_Q.append([Queue() for _ in range(MODEL.N_N_THREAD)])
            
        # potential_Q belongs to neurons
        self.potential_Q = []
        for _ in range(MODEL.N_N_THREAD) :
            # one more queue for exp.potential input - Final queue
            self.potential_Q.append([Queue() for _ in range(MODEL.N_S_THREAD+1)])

        print('Initiating Queues and Threads for Neurons')
        for i in range(MODEL.N_N_THREAD) :
            print('{0}/{1}'.format(i+1, MODEL.N_N_THREAD))
            pre_q_list = [r[i] for r in self.pre_Q]
            post_q_list = [r[i] for r in self.post_Q]
            self.n_procs.append(Process(
                target = tf.neuron_init,
                args = (
                    self.n_list[i*MODEL.N_NEURON:(i+1)*MODEL.N_NEURON],
                    pre_q_list,
                    post_q_list,
                    self.potential_Q[i],
                    self.barrier,
                    MODEL.N_SYNAPSE,
                    i,
                    TICKS,
                    TICKS - LOG_TICKS,
                )
            ))

        print('Initiating Queues and Threads for Synapses')
        for i in range(MODEL.N_S_THREAD) :
            print('{0}/{1}'.format(i+1, MODEL.N_S_THREAD))
            pot_q_list = [r[i] for r in self.potential_Q]
            self.s_procs.append(Process(
                target = tf.synapse_init,
                args = (
                    self.s_list[i*MODEL.N_SYNAPSE : (i+1)*MODEL.N_SYNAPSE],
                    self.pre_Q[i],
                    self.post_Q[i],
                    pot_q_list,
                    self.barrier,
                    MODEL.N_NEURON,
                    i,
                    TICKS,
                    TICKS - LOG_TICKS,
                )
            ))
        
        print('Initiating external potential thread')
        self.ext_pot_proc = Process(
            target = tf.ext_pot_init,
            args= (
                MODEL.ext_model,
                MODEL.ext_kwargs,
                [r[-1] for r in self.potential_Q],
                self.barrier,
                MODEL.N_NEURON,
                TICKS,
            )
        )
        # print('Initiating S_to_N_distributer')
        # self.s_n_dist = Process(
        #     target = tf.s_to_n_distributer,
        #     args = (
        #         self.n_potential_Q,
        #         self.s_potential_Q,
        #         MODEL.N_N_THREAD,
        #         MODEL.N_NEURON,
        #         MODEL.N_S_THREAD,
        #         TICKS,
        #         MODEL.ext_model,
        #         MODEL.ext_kwargs,
        #     )
        # )
        # print('Initiating N_to_S_distributer')
        # self.n_s_dist = Process(
        #     target= tf.n_to_s_distributer,
        #     args= (
        #         self.s_pre_Q,
        #         self.s_post_Q,
        #         self.n_pre_Q,
        #         self.n_post_Q,
        #         MODEL.N_S_THREAD,
        #         MODEL.N_SYNAPSE,
        #         MODEL.N_N_THREAD,
        #         TICKS,
        #     )
        # )

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
        print('Starting Neuron processes')
        for idx, n_p in enumerate(self.n_procs) :
            print('{0}/{1}'.format(idx+1,MODEL.N_N_THREAD))
            n_p.start()
        print('Starting Syapse processes')
        for idx, s_p in enumerate(self.s_procs) :
            print('{0}/{1}'.format(idx+1,MODEL.N_S_THREAD))
            s_p.start()
        print('Starting external potential process')
        self.ext_pot_proc.start()
        print('Simulation start')
        init_time = time.time()
        for _ in tqdm.trange(TICKS, ncols = 150, mininterval = 1, unit = 'tick') :
            self.barrier.wait()

        # self.s_n_dist.start()
        # self.n_s_dist.start()
        # total_potentials = []
        # total_pre = []
        # total_post = []
        # for _ in range(MODEL.N_N_THREAD):
        #     total_potentials.append([])
        # for _ in range(MODEL.N_S_THREAD) :
        #     total_pre.append([])
        #     total_post.append([])
        ####################################Tick#############
        # for t in range(TICKS) :
            # print('Tick : {}'.format(t+1))
            # external = MODEL.ext_model(**MODEL.ext_kwargs)
            # for n in external :
            #     total_potentials[n[-1]//MODEL.N_NEURON].append(n)

            # for idx, Q in enumerate(self.n_potential_Q) :
            #     Q.put(total_potentials[idx])

            # for idx in range(MODEL.N_S_THREAD) :
            #     self.s_pre_Q[idx].put(total_pre[idx])
            #     self.s_post_Q[idx].put(total_post[idx])

            #--------------------------------------------
            # for i in range(MODEL.N_N_THREAD):
            #     total_potentials[i] = []
            # for i in range(MODEL.N_S_THREAD) :
            #     total_pre[i] = []
            #     total_post[i] = []

            # for idx in range(MODEL.N_N_THREAD) :
            #     for pre in self.n_pre_Q[idx].get() :
            #         total_pre[pre[-1]//MODEL.N_SYNAPSE].append(pre)
            #     for post in self.n_post_Q[idx].get() :
            #         total_post[post[-1]//MODEL.N_SYNAPSE].append(post)
            # for idx in range(MODEL.N_S_THREAD) :
            #     for n in self.s_potential_Q[idx].get() :
            #         total_potentials[n[-1]//MODEL.N_NEURON].append(n)

        #########################################################
        # for Q in self.n_potential_Q :
        #     Q.put(MULTI_sentinel)
        # for Q in self.s_post_Q :
        #     Q.put(MULTI_sentinel)
        # for Q in self.s_pre_Q :
        #     Q.put(MULTI_sentinel)
        # neuron_log = []
        # synapse_log = []
        # while len(neuron_log) < N_N_THREAD :
        #     neuron_log.append(self.n_log_Q.get())
        # while len(synapse_log) < N_S_THREAD :
        #     synapse_log.append(self.s_log_Q.get())
        self.connection_logging()

        # self.s_n_dist.join()
        # self.n_s_dist.join()
        for n_p in self.n_procs :
            n_p.join()
        for s_p in self.s_procs :
            s_p.join()
        self.ext_pot_proc.join()
        print('total time : {:.2f}'.format(time.time()-init_time))

if __name__ == '__main__' :
    freeze_support()
    Main_multi().run()