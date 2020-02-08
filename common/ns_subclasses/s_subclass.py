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
    """
    def __init__(self, pre, post, ex_in_type, dopa_neurons : list, predict, ID_num : int):
        super().__init__(pre, post, ex_in_type, ID_num)
        self.t_dopa = 0
        self.predict = predict
        self.dopa_neurons = dopa_neurons

    def pre_fired(self, arg) :
        if arg == NT_DEFAULT :
            self.t_pre = self.time
            self.fired = True
        elif isinstance(arg, list) :
            if arg[0] == NT_DOPA :
                self.dopa_passed(arg[1])

    def post_fired(self, arg) :
        self.t_post = self.time

    def dopa_passed(self, amount) :
        self.weight = tools.dopa_weight_modify(
            self.t_pre - self.t_post,
            self.t_post - self.t_dopa,
            self.predict,
            amount,
            self.weight
        )

    def get_connection(self) :
        pre = self.dopa_neurons.copy()
        pre.append(self.pre_neuron)
        return [pre, self.post_neuron]

class S_Dopa_pre_only(S_Dopa_dependent) :
    """
    Same as S_Dopa_dependent,
    just this doesn't care post synaptic fire
    """
    def dopa_passed(self, amount) :
        self.weight = tools.dopa_weight_modify(
            1,
            self.t_pre - self.t_dopa - 2,
            self.predict,
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