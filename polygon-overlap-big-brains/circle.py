from particle import Particle
import pygame


class Circle(Particle):
    def __init__(self, radius=10, color=[0, 0, 0], **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos.int(), round(self.radius))
