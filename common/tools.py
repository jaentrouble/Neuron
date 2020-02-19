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
    delta_t += 1

    if delta_t <= -WEIGHT_t_0 or delta_t >= WEIGHT_t_0:
        return weight
    
    elif delta_t < 0 :
        # delta_t += 1
        delta = WEIGHT_tan_bias + delta_t*WEIGHT_tan
        return min(weight + delta, WEIGHT_max)

    elif delta_t >= 0 :
        delta = -WEIGHT_tan_bias + delta_t*WEIGHT_tan
        return max(weight + delta, 0)

def dopa_weight_modify(delta_prepost, delta_postdopa, dopa_q, weight) :
    """
    dopa_weight_modify
    delta_prepost : pre - post
    delta_postdopa : post - dopa
    predict : the time dopa should take to arrive
    dopa_q : quantity of dopamine
    """
    delta_prepost += 1
    delta_postdopa += 1
    delta_firedopa = delta_postdopa + max(delta_prepost, 0)

    if (
        delta_prepost <= -WEIGHT_t_0 or
        delta_prepost >= WEIGHT_t_0 or
        delta_firedopa <= -WEIGHT_t_0 or
        delta_firedopa >= 0
    ):
        # return min(max(weight + SYNAPSE_decay, 0), WEIGHT_max)
        return max(weight, 0)

    else :
        dopa = dopa_q - DOPA_normal
        if delta_prepost < 0 :
            weight_delta_pp = WEIGHT_dopa_pp + delta_prepost*WEIGHT_dopa_tan_pp
        elif delta_prepost >= 0 :
            weight_delta_pp = -WEIGHT_dopa_pp + delta_prepost*WEIGHT_dopa_tan_pp
            weight_delta_pp *= WEIGHT_dopa_in_ex_ratio
        
        weight_delta_pd = WEIGHT_dopa_pd + delta_firedopa*WEIGHT_dopa_tan_pd
        
        delta_weight = weight_delta_pp * weight_delta_pd * WEIGHT_F_max * WEIGHT_max * dopa/DOPA_normal
        return min(max(weight + delta_weight + SYNAPSE_decay, 0), WEIGHT_max)

def combi(n, k) :
    if k> n :
        return 0
    else :
        return int(math.factorial(n)/(math.factorial(k) * math.factorial(n-k)))

def split(lst, n, overlap = 0) :
    """
    splits given list into n equal segments.
    left overs will be evenly distributed.
    Segments keeps the order of the list.
    Overlaps to the next segment.
    """
    smallstep = len(lst)//n
    leftover = len(lst) % n
    div = [smallstep+1 if i<leftover else smallstep for i in range(n)]
    idx = 0
    chunks = []
    for step in div :
        chunks.append(lst[idx:idx+step+overlap])
        idx += step
    return chunks