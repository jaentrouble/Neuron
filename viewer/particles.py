import pygame
from common.constants import *
import numpy as np

def groupsetter(*groups) :
    Soma.groups = groups
    Dendrites.groups = groups

class Soma(pygame.sprite.Sprite) :
    """
    Soma
    Small Dots for Neurons
    potential update -> fired -> update
    """
    def __init__(self, pos : list) :
        """
        pos : centerx, centery
        """
        super().__init__(self.groups)
        self.image = pygame.Surface((VIEWER_soma_size, VIEWER_soma_size))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
        self.potential = NEURON_rest
        self.is_fired = False

    def potential_to_color (self, potential) :
        color_scale = min(255, int(255*(potential-NEURON_undershoot)/NEURON_threshold))
        return (color_scale, color_scale, color_scale)

    def potential_update (self, potential) :
        self.potential = potential

    def fired (self) :
        self.is_fired = True
        
    def update(self) :
        if self.is_fired:
            self.image.fill(VIEWER_fired_color)
            self.is_fired = False
        else :
            self.image.fill(self.potential_to_color(self.potential))

class Dendrites(pygame.sprite.Sprite) :
    """
    Dendrites
    A big transparant surface, drawing synapses as lines
    weight_update -> fired -> update
    """
    def __init__(self, connections : list, neuron_pos_list : list, screen_size : list) :
        super().__init__(self.groups)
        self.image = pygame.Surface(screen_size)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = 0, 0
        self.s_num = len(connections)
        self.connections = connections
        self.n_pos_list = neuron_pos_list
        self.converge_weight = (WEIGHT_g_max*SYNAPSE_decay)/(1-SYNAPSE_decay)
        self.weights = np.ones(self.s_num)
        self.is_fired = np.zeros(self.s_num)

    def weight_to_color(self, weight) :
        color_scale = min(255, int(255*weight/self.converge_weight))
        return (color_scale, color_scale, color_scale)

    def weight_update(self, weight_list : list) :
        for w in weight_list :
            self.weights[w[0]] = w[1]

    def fired(self, fired_list : list) :
        self.is_fired = np.zeros(self.s_num)
        for idx in fired_list :
            self.is_fired[idx] = True

    def update(self) :
        for idx, con in enumerate(self.connections) :
            if self.is_fired[idx]:
                pygame.draw.line(
                    self.image,
                    VIEWER_fired_color,
                    self.n_pos_list[con[0]],
                    self.n_pos_list[con[1]],
                    VIEWER_dendrite_thick,
                )
            else :
                pygame.draw.line(
                    self.image,
                    self.weight_to_color(self.weights[idx]),
                    self.n_pos_list[con[0]],
                    self.n_pos_list[con[1]],
                    VIEWER_dendrite_thick,
                )