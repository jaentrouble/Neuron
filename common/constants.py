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

LOG_path = 'log'
LOG_multi_neuron_name = 'log_neuron_thread_{}.json'
LOG_multi_synapse_name = 'log_synapse_thread_{}.json'
LOG_connection_name = 'log_connection.json'

#modifiable-------------------------------------------
SYNAPSE_decay = 0.001
SYNAPSE_default_weight = 1

DOPA_normal = 4
DOPA_max = 8

WEIGHT_max = 3
WEIGHT_F_max = 0.005 
WEIGHT_t_0 = 8

WEIGHT_dopa_pp = 2
WEIGHT_dopa_pd = 2
WEIGHT_dopa_constant = 1

NEURON_threshold = 5
NEURON_rest = 0
NEURON_undershoot = -1
NEURON_decay = 1

VIEWER_soma_size = 5
VIEWER_fired_color = (255,255,0)
VIEWER_dendrite_thick = 1