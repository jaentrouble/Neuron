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

def grid_pos_maker(left : int, top : int, space : int, columns : int, n : int):
    pos = []
    for i in range(n) :
        pos.append([
            i%columns * space + left,
            i//columns * space + top
        ])
    return pos

def dopa_test_v_1(cmbi_start, outpt_start, val_start, relay_start, gaba_start, dopa_start, reward_start, reward, width, height) :
    pos = []
    pos.extend(grid_pos_maker(10, 100, 10, 10, cmbi_start))
    pos.extend(grid_pos_maker(10, height//2 - 100, 10, 20, outpt_start - cmbi_start))
    pos.extend(grid_pos_maker(10, height - 20, 10, 10, val_start - outpt_start))
    pos.extend(grid_pos_maker(width//2, height - 100, 10, 20, relay_start - val_start))
    pos.extend(grid_pos_maker(width - 200, height - 100, 10, 10, gaba_start - relay_start))
    pos.extend(grid_pos_maker(width - 120, height//2 - 100, 10, 10, dopa_start - gaba_start))
    pos.extend(grid_pos_maker(width//2, 10, 10, 10, reward_start - dopa_start))
    pos.extend(grid_pos_maker(width-100, 10, 10, 10, reward))
    return pos