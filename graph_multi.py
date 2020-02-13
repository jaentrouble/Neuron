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
y_log_potsum_r = 0
y_log_potsum_nr = 0
ticks = log.get_max_tick()
s_len1 = len(x_log1[0])
for idx in range(MODEL.dopa_start, MODEL.reward_start + MODEL.reward) :
    tmp = []
    for tick in x_log1 :
        tmp.append(tick[idx][1])
    y_log1.append(tmp)

r_count = 0
nr_count = 0
for t, tick in enumerate(x_log1[:-2]) :
    if tick[MODEL.reward_start][1] > 0 :
        y_log_potsum_r += x_log1[t+2][MODEL.dopa_start][1]
        r_count += 1
    else :
        y_log_potsum_nr += x_log1[t+2][MODEL.dopa_start][1]
        nr_count += 1
print('rewarded average pot :', y_log_potsum_r/r_count)
print('nonrewarded average pot :', y_log_potsum_nr/((nr_count-3*r_count)/4))

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

y_log3 = []
s_len3 = len(x_log2[0])
for idx in range(
    s_len3 - (MODEL.reward * MODEL.dopa) - (MODEL.v_n * MODEL.dopa) - (MODEL.v_n*2) - (MODEL.v_n * MODEL.dopa),
    s_len3 - (MODEL.reward * MODEL.dopa) - (MODEL.v_n * MODEL.dopa) - (MODEL.v_n*2),
) :
    tmp = []
    for tick in x_log2 :
        tmp.append(tick[idx][1])
    y_log3.append(tmp)

fig = make_subplots(rows= 3, cols= 1)
for idx, record in enumerate(y_log1) :
    if idx < MODEL.dopa :
        name = 'Dopa'
    else :
        name = 'Reward'
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record, name= name), row = 1, col= 1)
fig.update_xaxes(title_text = 'Ticks', row = 1, col = 1)
fig.update_yaxes(title_text = 'Potential', row = 1, col = 1, range = [-19, 16])
for record in y_log2 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 2, col= 1)
for record in y_log3 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 3, col= 1)
fig.update_layout(template = 'plotly_dark', autosize = False, width = 1000, height = 1000)
fig.show()