from common.constants import *
import math
"""
functions to make positions of neurons of viewer
every functions should have parameter 'n' as the number of positions to make
"""

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