import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
from viewer import log_loader
from common.models import experiment_model as emodel
from common.constants import *
from common import tools
import csv
import time
from scipy import signal
MODEL = emodel.dopa_test_1


n_log_names = []
s_log_names = []
load_strt_time = time.time()
for i in range(MODEL.N_N_THREAD) :
    n_log_names.append(LOG_multi_neuron_name.format(i))
for i in range(MODEL.N_S_THREAD) :
    s_log_names.append(LOG_multi_synapse_name.format(i))
log = log_loader.Log(n_log_names, s_log_names, LOG_connection_name)
print('{} ticks of log loaded'.format(log.get_max_tick()+1))
print('{:.2f} seconds'.format(time.time() - load_strt_time))

######################### Customize
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
    
potsum_r = 0
potsum_r_p = 0
potsum_r_n = 0
potsum_nr = 0
potsum_nr_p = 0
potsum_nr_n = 0
potmax_r_p = 0
potmax_r_n = 0
potmax_nr_p = 0
potmax_nr_n = 0
r_count = 0
r_p_count = 0
r_n_count = 0
nr_count = 0
nr_p_count = 0
nr_n_count = 0
r_p_list = ['r_p']
r_n_list = ['r_n']
nr_p_list = ['nr_p']
nr_n_list = ['nr_n']
for t, tick in enumerate(x_log1[:-2]) :
    pot = x_log1[t+2][MODEL.dopa_start][1]
    if tick[MODEL.reward_start][1] > 0 :
        potsum_r += pot
        if pot > 0 :
            potsum_r_p += pot
            if pot > potmax_r_p :
                potmax_r_p = pot
            r_p_count += 1
            r_p_list.append(pot)
        elif pot < 0 :
            potsum_r_n += pot
            if pot < potmax_r_n :
                potmax_r_n = pot
            r_n_count += 1
            r_n_list.append(pot)
        r_count += 1
    else :
        potsum_nr += pot
        if pot > 0 :
            potsum_nr_p += pot
            if pot > potmax_nr_p :
                potmax_nr_p = pot
            nr_p_count += 1
            nr_p_list.append(pot)
        elif pot < 0 :
            potsum_nr_n += pot
            if pot < potmax_nr_n :
                potmax_nr_n = pot
            nr_n_count += 1
            nr_n_list.append(pot)
        nr_count += 1
print('rewarded average pot :{:.2f}'.format(potsum_r/r_count))
if r_p_count > 0 :
    print('rewarded positive Mean : {0:.2f}, Max : {1:.2f}'.format(potsum_r_p/r_p_count, potmax_r_p))
if r_n_count > 0 :
    print('rewarded negative Mean : {0:.2f}, Min : {1:.2f}'.format(potsum_r_n/r_n_count, potmax_r_n))
print('nonrewarded average pot :{:.2f}'.format(potsum_nr/((nr_count-3*r_count)/4)))
if nr_p_count > 0 :
    print('nonrewarded positive Mean : {0:.2f}, Max : {1:.2f}'.format(potsum_nr_p/nr_p_count, potmax_nr_p))
if nr_n_count > 0 :
    print('nonrewarded negative Mean : {0:.2f}, Min : {1:.2f}'.format(potsum_nr_n/nr_n_count, potmax_nr_n))
print('{:.2f} seconds passed'.format(time.time()-load_strt_time))

with open(os.path.join(LOG_path,'dopa_pot.csv'), 'w', newline= '') as csvfile :
    potwriter = csv.writer(csvfile)
    potwriter.writerow(r_p_list)
    potwriter.writerow(r_n_list)
    potwriter.writerow(nr_p_list)
    potwriter.writerow(nr_n_list)

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
        fig.add_trace(go.Scatter(x = list(range(ticks)), y = signal.savgol_filter(record,101,1), name= 'smooth'), row = 1, col= 1)
    else :
        name = 'Reward'
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record, name= name), row = 1, col= 1)
fig.update_xaxes(title_text = 'Ticks', row = 1, col = 1)
fig.update_yaxes(title_text = 'Potential', row = 1, col = 1,)
for record in y_log2 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 2, col= 1)
for record in y_log3 :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = record), row = 3, col= 1)
fig.update_layout(template = 'plotly_dark', autosize = False, width = 1000, height = 1000)
fig.show()
print('{:.2f} seconds passed'.format(time.time()-load_strt_time))
