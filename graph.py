import plotly.graph_objects as go
import pandas as pd
import numpy as np
import rapidjson
import os

with open(os.path.join('log','log_single.json'), 'r') as lf :
    log = rapidjson.load(lf)

log = np.array(log)
log = log.transpose()
# i = synapse, j = time
fig = go.Figure()
ticks = len(log[0])
for synapse_record in log :
    fig.add_trace(go.Scatter(x = list(range(ticks)), y = synapse_record))

fig.show()