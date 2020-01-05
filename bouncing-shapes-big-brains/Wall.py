from Vec2 import Vec2
import pygame
from particle import Particle


class Wall(Particle):
    def __init__(self, pos, normal, color=(0, 0, 0), length=1000):
        super().__init__(mass=float('inf'), pos=pos, vel=Vec2(0, 0))
        self.pos = pos
        self.normal = normal#.hat()
        self.length = length
        self.color = color
        self.mass = float('inf')
        self.vel = Vec2(0, 0)

    def draw(self, screen):
        disp = self.length*~self.normal
        start = self.pos - disp
        end = self.pos + disp
        pygame.draw.line(screen, self.color, start.int(), end.int())
