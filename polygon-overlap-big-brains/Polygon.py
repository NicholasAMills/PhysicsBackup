from particle import Particle
import pygame
import math


class Polygon(Particle):
    # offsets = list of displacements to reach the vertices
    def __init__(self, mass, pos, vel, offsets, color, width):
        super().__init__(mass=mass, pos=pos, vel=vel)
        self.offsets = offsets
        self.color = color
        self.width = width

        self.points = []
        for o in offsets:
            self.points.append(pos + o)

        self.normals = []
        for i in range(len(self.points)):
            normal = (self.points[i] - self.points[i - 1]).hat().perp()
            self.normals.append(normal)

    def draw(self, screen):
        points = []
        for p in self.points:
            points.append(p.int())
        pygame.draw.polygon(screen, self.color, self.points, self.width)

        # for i in range(len(self.normals)):
        #     pygame.draw.line(screen, (0, 0, 0), points[i], (self.points[i] + 50 * self.normals[i]).int())

    def update(self, dt):
        super().update(dt)
        self.update_points_normals()
        for i in range(len(self.points)):
            self.points[i] = self.pos + self.offsets[i]

    # define original_normals
    #     as what were normals before

    def update_points_normals(self):
        # Compute points from pos, angle and offsets
        self.angle=0
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        for i in range(len(self.points)):
            self.points[i] = self.pos + self.offsets[i] # .rotate_sin_cos(s, c)
            # self.normals[i] = self.original_normals[i] # .rotate_sin_cos(s, c)

    def translate(self, disp):
        super().translate(disp)
        self.update_points_normals()

    def add_impulse(self, impulse, pos=None):
        self.vel += impulse


'''
class UniformPolygon(Polygon):
    def __init__(self, offsets, density, pos, vel, angle, avel, color, width):
        # Compute Everything
        # Compute mass
        # A = the area of the triangle
        # A = 1 / 2 * Offsets_i cross product Offsets_i-1
        # Moment of inertia
        # I_i = m / 6 (|S_i|^2 + |S_i-1|^2 + S_i dot product S_i-1
        # Centroid of a triangle
        # R_i = 1 / 3(S_i + S_i-1)
        # Centroid of entire shape (weighted average)
        # R = m_i*R_i/m_i
        mass = density * A
        # Compute moment of inertia
        # Shift all offsets by -R
        # S_i += -R
        # I_offcenter = I_center + MR^2    M = mass
        super().__init__(offsets=offsets, mass=mass, pos=pos, vel=vel, angle=angle, avel=avel, color=color, width=width)
    # Need to correct pos so it spins around the centroid (Center of mass)
'''
