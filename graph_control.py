import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common.models import experiment_model as emodel
from common.constants import *
import numpy as np
import os
import rapidjson
MODEL = emodel.dopa_test_1

with open(os.path.join(LOG_path, LOG_control_name), 'r') as logfile:
    log = rapidjson.load(logfile)
td_log = log[str(CTL_TD_LOG)]
v_log = log[str(CTL_V_LOG)]
r_log = log[str(CTL_R_LOG)]
ticks = len(td_log)

########################### Customize

fig = make_subplots(rows = 2, cols = 1)

fig.add_trace(go.Scatter(x = np.arange(ticks), y= td_log, name = 'Dopa'), row=1, col=1)
fig.add_trace(go.Scatter(x = np.arange(ticks), y= r_log, name = 'Reward'), row=1, col=1)
for idx, state in enumerate(v_log) :
    fig.add_trace(go.Scatter(
        x = np.arange(ticks),
        y = state,
        name = 'V[{}]'.format(idx),
    ), row=2, col=1)
fig.update_layout(template = 'plotly_dark', autosize = False, width = 1000, height = 1000)
fig.show()