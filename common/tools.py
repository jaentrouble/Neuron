from common.constants import *
import math
import numpy as np

def weight_modify(delta_t : int, weight) :
    """
    weight_modify
    delta_t : pre - post
    weight will not exceed WEIGHT_max or get lower than 0
    updates weight
    returns new weight
    """
    delta_t -= 2

    if delta_t <= -WEIGHT_t_0 or delta_t >= WEIGHT_t_0:
        return weight
    
    elif delta_t < 0 :
        delta = (WEIGHT_F_max + (delta_t*WEIGHT_F_max)/WEIGHT_t_0) * WEIGHT_max
        return min(weight + delta, WEIGHT_max)

    elif delta_t >= 0 :
        delta = ((delta_t*WEIGHT_F_max)/WEIGHT_t_0 - WEIGHT_F_max) * WEIGHT_max
        return max(weight + delta, 0)

def dopa_weight_modify(delta_prepost, delta_postdopa, predict, dopa_q, weight) :
    """
    dopa_weight_modify
    delta_prepost : pre - post
    delta_postdopa : post - dopa
    predict : the time dopa should take to arrive
    dopa_q : quantity of dopamine
    """
    delta_prepost -= 2
    delta_postdopa -= predict

    if (
        delta_prepost <= -WEIGHT_t_0 or
        delta_prepost >= WEIGHT_t_0 or
        delta_postdopa <= -WEIGHT_t_0 or
        delta_postdopa >= WEIGHT_t_0
    ):
        return max(weight + SYNAPSE_decay, 0)
    else :
        dopa = dopa_q - DOPA_normal
        if delta_prepost < 0 :
            delta_prepost = WEIGHT_dopa_pp + (delta_prepost*WEIGHT_dopa_pp)/WEIGHT_t_0
        elif delta_prepost >= 0 :
            delta_prepost = -WEIGHT_dopa_pp + (delta_prepost*WEIGHT_dopa_pp)/WEIGHT_t_0
        
        if delta_postdopa < 0 :
            delta_postdopa = WEIGHT_dopa_pp + (delta_postdopa*WEIGHT_dopa_pp)/WEIGHT_t_0
        elif delta_postdopa >= 0 :
            delta_postdopa = -WEIGHT_dopa_pp + (delta_postdopa*WEIGHT_dopa_pp)/WEIGHT_t_0
        
        if delta_prepost < 0 and delta_postdopa < 0 :
            sign = -1
        else :
            sign = 1
        
        delta_weight = delta_prepost * delta_postdopa * WEIGHT_F_max * WEIGHT_max * dopa/DOPA_normal * sign
        return max(weight + delta_weight + SYNAPSE_decay, 0)

def combi(n, k) :
    if k> n :
        return 0
    else :
        return int(math.factorial(n)/(math.factorial(k) * math.factorial(n-k)))

def split(lst, n) :
    smallstep = len(lst)//n
    leftover = len(lst) % n
    div = [smallstep+1 if i<leftover else smallstep for i in range(n)]
    idx = 0
    chunks = []
    for step in div :
        chunks.append(lst[idx:idx+step])
        idx += step
    return chunks