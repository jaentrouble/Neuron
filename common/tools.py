from common.constants import *
import math

def weight_modify(delta_t : int, weight) :
    """
    weight_modify
    delta_t : pre - post
    g will not exceed gmax
    updates weight and g
    returns weight, g
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

def ellipse_pos_maker(a : int, b: int, center : list, n : int) :
    """
    ellipse_pos_maker
    makes n points on a ellipse(x : a, y : b, center : center)
    positions will be in integers
    """
    pos = []
    for i in range(n) :
        pos.append([
            int(center[0] + a*math.cos(i*2*math.pi/n)),
            int(center[1] + b*math.sin(i*2*math.pi/n)),
        ])
    return pos