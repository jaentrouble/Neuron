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
    def __init__(self, pre, post, predict, ID_num : int):
        super().__init__(pre, post, SYNAPSE_excitatory, ID_num)
        self.t_dopa = 0
        self.predict = predict

    def pre_fired(self, arg) :
        if arg == NT_DEFAULT :
            self.t_pre = self.time
            self.fired = True
        elif isinstance(arg, list) :
            if arg[0] == NT_DOPA :
                self.dopa_passed(arg[1])

    def dopa_passed(self, amount) :
        self.weight = tools.dopa_weight_modify(
            self.t_pre - self.t_post,
            self.t_post - self.t_dopa,
            self.predict,
            amount,
            self.weight
        )