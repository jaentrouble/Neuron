from common.ns_subclasses.neuron import Synapse
from common.constants import *
from common import tools

class S_Dopa_dependent(Synapse) :
    """
    S_Dopa
    only strengthens when DOPA comes
    Pre - Post -Target time passed-> Dopa
    it will decade too, so constant DOPA is needed
    Dopa should be handed over as
    [NT_DOPA, amount] through 'arg' parameter of 'pre-fired' method
    will return discounted weight to the next neuron
    """
    def __init__(self, pre, post, ex_in_type, dopa_neurons : list, ID_num : int, discount = 1, init_weight = SYNAPSE_default_weight):
        super().__init__(pre, post, ex_in_type, ID_num, init_weight = init_weight)
        self.t_dopa = 0
        self.dopa_neurons = dopa_neurons
        self.discount = discount

    def pre_fired(self, arg) :
        if arg[0] == NT_DEFAULT :
            self.t_pre = self.time
            self.fired = True
        elif arg[0] == NT_DOPA :
            self.dopa_passed(arg[1])

    def post_fired(self, arg) :
        self.t_post = self.time

    def dopa_passed(self, amount) :
        self.t_dopa = self.time
        self.weight = tools.dopa_weight_modify(
            self.t_pre - self.t_post,
            self.t_post - self.t_dopa - 2, # timing adjustment
            amount,
            self.weight
        )


    def get_connection(self) :
        pre = self.dopa_neurons.copy()
        pre.append(self.pre_neuron)
        return [pre, self.post_neuron]

    def get_signal(self):
        wt = list(super().get_signal())
        wt[0] *= self.discount
        return wt

class S_Dopa_pre_only(S_Dopa_dependent) :
    """
    Same as S_Dopa_dependent,
    just this doesn't care post synaptic fire
    """
    def dopa_passed(self, amount) :
        self.t_dopa = self.time
        self.weight = tools.dopa_weight_modify(
            -2,
            self.t_pre - self.t_dopa,
            amount,
            self.weight,
        )

class S_non_decaying(Synapse) :
    """
    S_non-decaying
    Simple synapse, but not decaying
    """
    def tick(self) :
        self.time += 1

class S_relay(Synapse) :
    """
    S_relay
    transfers signal, no weight change
    """
    def tick(self) :
        pass

    def pre_fired(self, arg) :
        self.fired = True

    def post_fired(self, arg) :
        pass
