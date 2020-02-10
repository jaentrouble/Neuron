import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

x_log1 = log.get_total_pot_log()
x_log2 = log.get_total_wt_log()

y_log1 = []
ticks = log.get_max_tick()
s_len1 = len(x_log1[0])
for idx in range(MODEL.dopa_start, MODEL.reward_start + MODEL.reward) :
    tmp = []
    for tick in x_log1 :
        tmp.append(tick[idx][1])
    y_log1.append(tmp)

y_log2 = []
s_len2 = len(x_log2[0])
for idx in range(
    s_len2-(MODEL.reward * MODEL.dopa) - (MODEL.v_n * MODEL.dopa),
    s_len2-(MODEL.reward * MODEL.dopa)
):
    tmp = []
    for tick in x_log2 :
        tmp.append(tick[idx][1])
    y_log2.append(tmp)

fig = make_subplots(rows= 2, cols= 1)
for record in y_log1 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 1, col= 1)
for record in y_log2 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 2, col= 1)
fig.show()