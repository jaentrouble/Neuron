from constants import *

def weight_modify(delta_t : int, weight, g) :
    """
    weight_modify
    delta_t : pre - post
    g will not exceed gmax
    updates weight and g
    returns weight, g
    """
    delta_t -= 2

    if delta_t <= -WEIGHT_t_0 or delta_t >= WEIGHT_t_0:
        return weight + g, g
    
    elif delta_t < 0 :
        new_g = min((WEIGHT_F_max + (delta_t*WEIGHT_F_max)/WEIGHT_t_0) * WEIGHT_g_max + g, WEIGHT_g_max)
        return weight + new_g, new_g

    elif delta_t >= 0 :
        new_g = max(((delta_t*WEIGHT_F_max)/WEIGHT_t_0 - WEIGHT_F_max) * WEIGHT_g_max + g , 0)
        return weight + new_g, new_g