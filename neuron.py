import numpy
from constants import *

class Neuron():
    def __init__(self) :
        self.in_synapses = []
        self.ex_synapses = []

class Synapse() :
    """
    Synapse
    Multiply weight and send to post synaptic neuron
    """
    def __init__(self, pre : Neuron, post : Neuron) :
        self.pre_neuron = pre
        self.post_neuron = post
        self.weight = SYNAPSE_default_weight