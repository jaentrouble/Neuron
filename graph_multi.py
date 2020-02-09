import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from viewer import log_loader
from common.models import experiment_model as emodel
from common.constants import *
from common import tools
MODEL = emodel.dopa_test_1


n_log_names = []
s_log_names = []
for i in range(MODEL.N_N_THREAD) :
    n_log_names.append(LOG_multi_neuron_name.format(i))
for i in range(MODEL.N_S_THREAD) :
    s_log_names.append(LOG_multi_synapse_name.format(i))
log = log_loader.Log(n_log_names, s_log_names, LOG_connection_name)
print('{} ticks of log loaded'.format(log.get_max_tick()+1))

x_log = log.get_total_pot_log()
# x_log = log.get_total_wt_log()

y_log = []
ticks = log.get_max_tick()
s_len = len(x_log[0])
for idx in range(MODEL.dopa_start, MODEL.reward_start + MODEL.reward) :
# for idx in range(
#     s_len-(MODEL.reward * MODEL.dopa) - (MODEL.v_n * MODEL.dopa),
#     s_len-(MODEL.reward * MODEL.dopa)
# ):
    tmp = []
    for tick in x_log :
        tmp.append(tick[idx][1])
    y_log.append(tmp)

fig = go.Figure()
for record in y_log :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record))

fig.show()