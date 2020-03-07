SYNAPSE_pre_fired = 0
SYNAPSE_post_fired = 1
SYNAPSE_not_fired_yet = -1
SYNAPSE_excitatory = 1
SYNAPSE_inhibitory = -1

NT_DEFAULT = None
NT_DOPA = 0

MULTI_sentinel = -1
MULTI_potent_log = 0
MULTI_fired_neuron_log = 1
MULTI_weight_log = 2
MULTI_fired_synapse_log = 3

CTL_TD_LOG = 0
CTL_V_LOG = 1
CTL_R_LOG = 2

LOG_path = 'log'
LOG_multi_neuron_name = 'log_neuron_thread_{}.json'
LOG_multi_synapse_name = 'log_synapse_thread_{}.json'
LOG_connection_name = 'log_connection.json'
LOG_control_name = 'log_control.json'

RANDOM_SEED = 0

#modifiable-------------------------------------------
SYNAPSE_decay = 0.0001
SYNAPSE_default_weight = 1

DOPA_normal = 4
DOPA_max = 8

WEIGHT_max = 3
WEIGHT_F_max = 0.005
WEIGHT_t_0 = 16
WEIGHT_tan = (WEIGHT_F_max * WEIGHT_max)/WEIGHT_t_0
WEIGHT_tan_bias = WEIGHT_F_max * WEIGHT_max

WEIGHT_dopa_pp = 2
WEIGHT_dopa_pd = 2
WEIGHT_dopa_constant = 1
WEIGHT_dopa_in_ex_ratio = 1
WEIGHT_dopa_tan_pp = WEIGHT_dopa_pp/WEIGHT_t_0
WEIGHT_dopa_tan_pd = WEIGHT_dopa_pd/WEIGHT_t_0

NEURON_threshold = 4
NEURON_rest = 0
NEURON_undershoot = -1
NEURON_decay = 0.3

VIEWER_soma_size = 5
VIEWER_fired_color = (255,255,0)
VIEWER_dendrite_thick = 1