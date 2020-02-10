from common.models import synapse_models as smodel
from common.models import viewer_pos_models as vmodel
from common.models import ext_pot_models as epmodel
from common.models import neuron_models as nmodel
from common import tools
from common.constants import *

"""
class CLASSNAME () :
    N_N_THREAD =
    N_S_THREAD =
    N_NEURON =
    N_SYNAPSE =
    
    n_model = 
    n_kwargs = {

    }
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
    N_SYNAPSE = 1500
    N_NUM = N_NEURON * N_N_THREAD
    S_NUM = N_SYNAPSE * N_S_THREAD
    # Excitatory synapse percentage
    S_E_percent = 1
    # N of neurons to give External input
    EXTERNAL_N_neuron = 10
    EXTERNAL_potential = 20

    n_model = nmodel.simple_neurons
    n_kwargs = {
        'N_num' : N_NUM,
    }

    s_model = smodel.random_synapses
    s_kwargs = {
        'S_num' : S_NUM,
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
    FPS = 30
    v_model = vmodel.ellipse_pos_maker
    v_kwargs = {
        'a' : int(WIDTH/2 - 20),
        'b' : int(HEIGHT/2 - 20),
        'center' : [WIDTH/2, HEIGHT/2],
        'n' : N_NUM,
    }

class dopa_test_1 () :
    inpt_n = 10
    combi_r = 5
    outpt = 9
    v_n = 63
    dopa = 1
    reward = 1

    inpt_pot_n = 5
    rwrd_limit = 3

    N_N_THREAD = 2
    N_S_THREAD = 4
    N_NEURON = 250
    N_SYNAPSE = 600
    cmbi_start = inpt_n
    outpt_start = cmbi_start + tools.combi(inpt_n, combi_r)
    val_start = outpt_start + outpt
    relay_start = val_start + v_n
    gaba_start = relay_start + v_n
    dopa_start = gaba_start + v_n
    reward_start = dopa_start + dopa

    n_model = nmodel.dopa_test_n_1
    n_kwargs = {
        'inpt_n' : inpt_n,
        'combi_r' : combi_r,
        'outpt' : outpt,
        'v_n' : v_n,
        'dopa' : dopa,
        'reward' : reward,
    }
    s_model = smodel.dopa_test_s_1
    s_kwargs = {
        'inpt_n' : inpt_n,
        'combi_r' : combi_r,
        'outpt' : outpt,
        'v_n' : v_n,
        'dopa' : dopa,
        'reward' : reward,
    }
    ext_model = epmodel.dopa_test_e_1
    ext_kwargs = {
        'inpt_strt' : 0,
        'inpt_next_strt' : inpt_n,
        'n' : inpt_pot_n,
        'rwrd_limit' : rwrd_limit,
        'rwrd_strt' : reward_start,
        'rwrd_next_strt' : reward_start + reward,
        'potential' : NEURON_threshold + 1
    }
    # Viewer Settings ###########################

    WIDTH = 1000
    HEIGHT = 800
    FPS = 4
    v_model = vmodel.dopa_test_v_1
    v_kwargs = {
        'cmbi_start' : cmbi_start, 
        'outpt_start' : outpt_start, 
        'val_start' : val_start, 
        'relay_start' : relay_start,
        'gaba_start' : gaba_start, 
        'dopa_start' : dopa_start, 
        'reward_start' : reward_start, 
        'reward' : reward, 
        'width' : WIDTH, 
        'height' : HEIGHT,
    }
