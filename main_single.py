from common import neuron
from common.constants import *
import random
import rapidjson
import os
"""
Every Neurons and Synapses are called as their index (or ID)
"""

n_list = []
s_list = []

N_n = 100
N_s = 1000

for i in range(N_n) :
    n_list.append(neuron.Neuron(i))

for j in range(N_s) :
    pre = random.randrange(0,N_n)
    post = random.randrange(0,N_n)
    n_list[pre].connect_ex_one(j)
    n_list[post].connect_in_one(j)
    if random.random()<1 :
        s_list.append(neuron.Synapse(pre, post, SYNAPSE_excitatory, j))
    else :
        s_list.append(neuron.Synapse(pre, post, SYNAPSE_inhibitory, j))

t = 1000
input_neurons = n_list[:10]
# inhibit_neurons = n_list[-5:]
log = []
pre_fired = []
post_fired = []
fired_to_neurons = []

for loop in range(t) :

    for n in n_list :
        n.tick()
    for s in s_list :
        s.tick()
    
    # 1
    for n in n_list :
        if n.is_fired() :
            i, e = n.get_signal()
            pre_fired.extend(e)
            post_fired.extend(i)

    #3
    for s in s_list :
        if s.is_fired() :
            fired_to_neurons.append(s.get_signal())

    #2
    for s_index in post_fired :
        s_list[s_index].post_fired()
    for s_index in pre_fired :
        s_list[s_index].pre_fired()

    #4
    for n in fired_to_neurons :
        n_list[n[1]].input_potential(n[0])

    pre_fired = []
    post_fired = []
    fired_to_neurons = []

    #4.5
    if random.random() < 1 :
        for n in input_neurons :
            n.input_potential(50)
    # if random.random() < 0.2 :
    #     for n in inhibit_neurons :
    #         n.input_potential(-10)

    print('tick : ', loop)
    print(s_list[0].get_weight())
    tmp = []
    for s in s_list :
        tmp.append(s.get_weight())
    log.append(tmp)
reduced = 0
topped = 0
for s in s_list :
    if s.get_weight() <SYNAPSE_default_weight :
        reduced += 1
    elif s.get_weight() > (SYNAPSE_default_weight + WEIGHT_max)/2 :
        topped += 1

print('reduced : ',reduced)
print('topped : ', topped)

with open(os.path.join(LOG_path,'log_single.json'), 'w') as logfile :
    rapidjson.dump(log,logfile)