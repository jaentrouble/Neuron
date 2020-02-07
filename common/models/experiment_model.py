from common.models import synapse_models as smodel
from common.models import viewer_pos_models as vmodel
from common.models import ext_pot_models as epmodel

"""
class CLASSNAME () :
    N_N_THREAD =
    N_S_THREAD =
    N_NEURON =
    N_SYNAPSE =
    N_NUM = N_NEURON * N_N_THREAD
    S_NUM = N_SYNAPSE * N_S_THREAD

    s_model =
    s_kwargs = {
        
    }
    ext_model =
    ext_kwargs = {

    }
# Viewer Settings ###########################

    WIDTH =
    HEIGHT =
    FPS =
    v_model =
    v_kwargs = {

    }
"""

class random_test_1() :
    #Numbers of Threads to (N)eurons and (S)ynapses
    N_N_THREAD = 1
    N_S_THREAD = 4
    # numbers per Thread
    N_NEURON = 100
    N_SYNAPSE = 300
    N_NUM = N_NEURON * N_N_THREAD
    S_NUM = N_SYNAPSE * N_S_THREAD
    # Excitatory synapse percentage
    S_E_percent = 1
    # N of neurons to give External input
    EXTERNAL_N_neuron = 10
    EXTERNAL_potential = 20

    s_model = smodel.random_synapses
    s_kwargs = {
        'S_num' : N_S_THREAD * N_SYNAPSE,
        'ex_percent' : S_E_percent,
        'N_num' : N_NUM
    }

    ext_model = epmodel.random_fixed_n_potentials
    ext_kwargs = {
        'n' : EXTERNAL_N_neuron,
        'n_num' : N_NUM,
        'potential' : EXTERNAL_potential,
    }

# Viewer Settings ###########################
    WIDTH = 1000
    HEIGHT = 800
    FPS = 10
    v_model = vmodel.ellipse_pos_maker
    v_kwargs = {
        'a' : int(WIDTH/2 - 20),
        'b' : int(HEIGHT/2 - 20),
        'center' : [WIDTH/2, HEIGHT/2],
        'n' : N_NUM,
    }

class dopa_test_1 () :
    N_N_THREAD = 1
    N_S_THREAD = 1
    N_NEURON = 10+10+252+252+252+1+1
    N_SYNAPSE = 10*252 + 252*10 + 252 + 252+252+252+252+1
    N_NUM = N_NEURON * N_N_THREAD
    S_NUM = N_SYNAPSE * N_S_THREAD

    s_model =
    s_kwargs = {
        
    }
    ext_model =
    ext_kwargs = {

    }
# Viewer Settings ###########################

    WIDTH =
    HEIGHT =
    FPS =
    v_model =
    v_kwargs = {

    }
