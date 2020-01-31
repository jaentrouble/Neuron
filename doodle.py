from OpenGL.GL import *
from OpenGL.GLU import *

import pygame

verticies = (
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1),
)

edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(4,6),(6,7),(5,1),(5,4),(5,7))

def Cube() :
    for edge in edges :
        glBegin(GL_LINES)
        for vertex in edge :
            glVertex3fv(verticies[vertex])
        glEnd()

pygame.init()
screen = pygame.display.set_mode((500,500), pygame.DOUBLEBUF | pygame.OPENGL)

gluPerspective(60, (500/500), 0.1, 100)

glTranslatef(0,0,-5)

glRotatef(0,0,0,0)

clock = pygame.time.Clock()

while True :
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    