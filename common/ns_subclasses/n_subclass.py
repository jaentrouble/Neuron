from common.ns_subclasses.neuron import Neuron
from common.constants import *

class N_Dopa_emit(Neuron) :
    """
    N_Dopa
    emits dopamine to synapses
    get_signal will return list of [[NT_DOPA, amount],idx]
    Note that this neuron is always firing something
    """
    def __init__(self, ID_num : int) :
        super().__init__(ID_num)

    def is_fired(self) :
        return True
        
    def get_signal(self) :
        """
        returns list of [[NT_DOPA, amount], idx] for ex synapses
        amount is proportion to the potential
        """
        s_in = []
        s_ex = []
        if self.potential >= NEURON_threshold :
            for s in self.in_synapses :
                s_in.append([NT_DEFAULT, s])
        for s in self.ex_synapses :
            s_ex.append([
                [
                    NT_DOPA,
                    max(min(DOPA_max, DOPA_normal + self.potential - NEURON_rest), 0)
                ],
                s,
            ])
        self.potential = NEURON_rest
        return s_in, s_ex

class N_AND_gate(Neuron) :
    """
    N_AND_gate
    If any potential comes in, it fires
    """
    def __init__(self, ID_num : int) :
        super().__init__(ID_num)
        self.fired = False

    def input_potential(self, potential) :
        self.fired = True

    def is_fired(self) :
        return self.fired

    def get_signal(self) :
        """
        get_signal
        Note that this neuron is an AND gate
        """
        self.fired = False
        return super().get_signal()