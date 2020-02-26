import tensorflow as tf
from tensorflow import keras
from common.constants import *
import numpy as np

"""
functions that define model and run them.
log & return data
"""

def dopa_test_c_1(ext_model, ext_kwargs, run_n, gamma) :
    """
    simple linear TD model
    """
    inpt_strt = ext_kwargs['inpt_strt']
    inpt_next_strt = ext_kwargs['inpt_next_strt']
    inpt_n = inpt_next_strt - inpt_strt
    rwrd_strt = ext_kwargs['rwrd_strt']
    rwrd_next_strt = ext_kwargs['rwrd_next_strt']
    inputs = keras.Input(shape = (inpt_n))
    outputs = keras.layers.Dense(1)(inputs)
    model = keras.Model(inputs = inputs, outputs = outputs)
    model.compile(
        loss = keras.losses.MeanSquaredError(),
        optimizer = keras.optimizers.Adam(),
        metrics = ['MeanSquaredError'],
    )
    sp_mask = np.zeros(inpt_n)
    next_reward = 0
    for _ in range(4) :
        for t in ext_model(**ext_kwargs) :
            if t[1] in range(inpt_strt, inpt_next_strt) :
                sp_mask[t[1]-inpt_strt] = 1
            elif t[1] in range(rwrd_strt, rwrd_next_strt) :
                next_reward = 1

    TD_log = []
    V_log = []
    tmp1, tmp2 = np.meshgrid(
        np.arange(inpt_n),
        np.arange(ext_kwargs['n']),
        indexing = 'ij'
    )
    tmp3 = (tmp1 + tmp2) % 10
    V_log_template = np.zeros((inpt_n, inpt_n))
    for idx, row in enumerate(V_log_template) :
        row[tmp3[idx]] = 1

    for _ in range(run_n) :
        s_mask = sp_mask
        reward = next_reward
        sp_mask = np.zeros(inpt_n)
        next_reward = 0
        for _ in range(4) :
            for t in ext_model(**ext_kwargs) :
                if t[1] in range(inpt_strt, inpt_next_strt) :
                    sp_mask[t[1]-inpt_strt] = 1
                elif t[1] in range(rwrd_strt, rwrd_next_strt) :
                    next_reward = 1
        v = model(np.array([s_mask]))
        vp = model(np.array([sp_mask]))
        model.fit(np.array([s_mask]), reward + gamma * vp)
        TD_log.append(float(gamma*vp - v))
        V_log.append(list(model(V_log_template)))

    print(TD_log)
    print(V_log)
