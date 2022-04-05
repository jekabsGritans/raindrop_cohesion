import pygame, sys
import random
import numpy as np
from math import hypot
from itertools import combinations

PARTICLES = 100
g = 9.81e-2

#setup
pygame.init()
clock = pygame.time.Clock()

#screen
screen_width = 800
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Raindrops")

def acc(r):
    t = -r**2*1.5
    Fg = g*r**3*1.5
    a = (t+Fg)/r**3
    return max(0.0, a)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, r):
        super().__init__()
        self._coords = np.array([x, y])
        self._r = r
        self._color = color
        self._v = np.array([0.0,0.0])
        self._a = np.array([0.0,0.0])
        self.update()
       
    def update(self):
        self._coords += (pygame.mouse.get_pos() - self._coords) / 100
        self._coords = self._coords + self._v
        self._a = np.array([0.0,acc(self._r)]) 
        self._v = self._v + self._a
        self.image = pygame.Surface([2*self._r, 2*self._r])
        self.image.set_alpha(128)
        pygame.draw.circle(self.image, self._color, (self._r, self._r), self._r)
        self.rect = self.image.get_rect()
        self.rect.center = tuple(self._coords)
        if self._coords[1] > screen_height:
            self.kill()
    
    def interact(self, other):
        if hypot(*(self._coords - other._coords)) < self._r+other._r:
            if other._r > self._r:
                self._coords = other._coords
            self._r = hypot(self._r, other._r)
            self.update()
            other.kill()
            

particles = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for _ in range(random.randint(1,3)):#range(PARTICLES - len(particles)):
        x = random.random() * screen_width
        y = random.random() * screen_height
        p = Particle(x, y, pygame.Color("cyan"), random.randint(4,10))
        particles.add(p)

    for p1, p2 in combinations(particles, 2):
        p1.interact(p2)

    particles.update()
    pygame.display.flip()
    screen.fill(pygame.Color("white"))
    particles.draw(screen)
    clock.tick(60)