from constants import *
import tools

class Neuron():
    """
    Neuron
    Sums up all inputs and if over threshold, shoots signal
    If shoot, will also tell in-synapse that it fired. (For weight update)
    """
    def __init__(self, ID_num : int) :
        self.in_synapses = []
        self.ex_synapses = []
        self.id = ID_num
        self.potential = NEURON_rest

    def tick(self, ):
        if self.potential > NEURON_rest + NEURON_decay :
            self.potential -= NEURON_decay
        elif self.potential < NEURON_rest-NEURON_decay :
            self.potential += NEURON_decay
        elif self.potential <= NEURON_rest + NEURON_decay and self.potential >= NEURON_rest-NEURON_decay :
            self.potential = NEURON_rest

    def connect_in_one(self, synapse) :
        """
        connect_in_one
        appends a synapse to in_synapses
        """
        self.in_synapses.append(synapse)

    def connect_in_list(self, synapse_list : list) :
        """
        connect_in_list
        extends the list of synapses to input
        """
        self.in_synapses.extend(synapse_list)

    def connect_ex_one(self, synapse):
        """
        connect_ex_one
        appends a synapse to ex_synapses
        """
        self.ex_synapses.append(synapse)

    def connect_ex_list(self, synapse_list : list) :
        """
        connect_ex_list
        extends the list of synapses to output
        """
        self.ex_synapses.extend(synapse_list)

    def input_potential(self, potential) :
        """
        input_potential
        adds potential to self.potential
        """
        self.potential += potential

    def is_fired(self) :
        if self.potential>= NEURON_threshold :
            return True
        else :
            return False

    def get_signal(self) :
        """
        get_signal
        Caution : Does not check if potential is higher than threshold
        use is_fired first
        returns in-synapse list, ex-synapse list and resets potential to undershoot
        """
        self.potential = NEURON_undershoot
        return self.in_synapses.copy(), self.ex_synapses.copy()

class Synapse() :
    """
    Synapse
    Multiply weight and send to post synaptic neuron
    Will count how many ticks have passed between 
    the synaptic transmission to the post-synapse neuron firing
    """
    def __init__(self, pre , post , neuron_type : int , ID_num : int) :
        """
        Synapse
        neuron_type : inhibitory or excitatory
        """
        # self.pre_neuron = pre
        self.post_neuron = post
        self.neuron_type = neuron_type
        self.weight = SYNAPSE_default_weight
        self.g = SYNAPSE_default_g
        self.time = 0
        self.id = ID_num
        self.t_pre = 0
        self.t_post = 0
        self.fired = False

    def tick(self, ):
        self.time += 1
        if self.neuron_type == SYNAPSE_excitatory :
            self.weight *= SYNAPSE_decay

    def pre_fired(self,):
        self.t_pre = self.time
        if self.neuron_type == SYNAPSE_excitatory :
            self.weight, self.g = tools.weight_modify(self.t_pre - self.t_post, self.weight, self.g)
        self.fired = True

    def post_fired(self, ):
        self.t_post = self.time
        if self.neuron_type == SYNAPSE_excitatory :
            self.weight, self.g = tools.weight_modify(self.t_pre - self.t_post, self.weight, self.g)

    def is_fired(self,) :
        return self.fired

    def get_signal(self, ):
        self.fired = False
        return self.neuron_type * self.weight, self.post_neuron

    def get_weight(self) :
        return self.weight