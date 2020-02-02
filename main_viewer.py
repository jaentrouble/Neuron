import pygame
from viewer import log_loader
from viewer import particles
from common.constants import *

class Main() :
    """
    Main
    """
    def __init__(self, n_thread_num : int, s_thread_num : int, fps = 60, width = 800, height = 600) :

        print('start loading')
        n_log_names = []
        s_log_names = []
        for i in range(n_thread_num) :
            n_log_names.append(LOG_multi_neuron_name.format(i))
        for i in range(s_thread_num) :
            s_log_names.append(LOG_multi_synapse_name.format(i))
        self.log = log_loader.Log(n_log_names, s_log_names, LOG_connection_name)
        print('loaded')

        pygame.init()
        self.allgroup = pygame.sprite.Group()
        self.width, self.height = width, height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rect = self.screen.get_rect()
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.convert()
        self.clock = pygame.time.Clock()

    def neuron_creator(self) :
        self.neurons = []
        self.neuron_pos = []
        

    def groupsetter(self) :
        particles.groupsetter(self.allgroup)

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.dendrites = particles.Dendrites(self.log.get_connections(), [], [self.width, self.height])

if __name__ == '__main__' :
    Main(2,4)