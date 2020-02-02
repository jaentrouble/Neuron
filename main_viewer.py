import pygame
from viewer import log_loader
from viewer import particles
from common.constants import *
from common import tools

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
        print('{} ticks of log loaded'.format(self.log.get_max_tick()+1))

        pygame.init()
        self.allgroup = pygame.sprite.Group()
        self.width, self.height = width, height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.rect = self.screen.get_rect()
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.convert()
        self.clock = pygame.time.Clock()
        self.groupsetter()
        self.tick = 0
        self.max_tick = self.log.get_max_tick()

    def neuron_creator(self) :
        self.neurons = []
        self.neuron_pos = tools.ellipse_pos_maker(
            int(self.width/2 - 20),
            int(self.height/2 - 20),
            [self.rect.centerx, self.rect.centery],
            self.log.get_n_num(),
        )
        for pos in self.neuron_pos :
            self.neurons.append(particles.Soma(pos))

    def groupsetter(self) :
        particles.groupsetter(self.allgroup)

    def update_particles(self, tick) :
        l = self.log.get_log(tick)
        for pot in l[MULTI_potent_log] :
            self.neurons[pot[0]].potential_update(pot[1])
        for idx in l[MULTI_fired_neuron_log] :
            self.neurons[idx].fired()
        for n in self.neurons :
            n.update()
        
        self.dendrites.weight_update(l[MULTI_weight_log])
        self.dendrites.fired(l[MULTI_fired_synapse_log])
        self.dendrites.update()

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.neuron_creator()
        self.dendrites = particles.Dendrites(self.log.get_connections(), self.neuron_pos, [self.width, self.height])
        self.play = False
        while mainloop :
            self.clock.tick(self.fps)
            ####escape########
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                    break
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False
                        break
            ########################

                    # start/stop
                    elif event.key == pygame.K_SPACE :
                        self.play = not self.play
            if self.play and self.tick <= self.max_tick:
                self.update_particles(self.tick)
                self.allgroup.clear(self.screen, self.background)
                self.allgroup.draw(self.screen)
                self.tick += 1
            cap = '{0} / {1} ticks'.format(self.tick+1, self.max_tick+1)
            pygame.display.set_caption(cap)
            pygame.display.flip()


if __name__ == '__main__' :
    Main(1,4, fps= 10, width = 600, height= 600).run()