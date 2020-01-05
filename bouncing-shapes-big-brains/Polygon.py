from particle import Particle
import pygame
import math
from Vec2 import Vec2


class Polygon(Particle):
    # offsets = list of displacements to reach the vertices
    def __init__(self, mass, pos, vel, offsets, color, width, momi, angle, avel):
        super().__init__(mass=mass, pos=pos, vel=vel, momi=momi, angle=angle, avel=avel)
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

        self.original_normals = self.normals.copy()
        self.update_points_normals()


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

    def update_points_normals(self):
        # Compute points from pos, angle and offsets
        s = math.sin(self.angle)
        c = math.cos(self.angle)
        for i in range(len(self.points)):
            self.points[i] = self.pos + self.offsets[i].rotated(s, c)
            self.normals[i] = self.original_normals[i].rotated(s, c)

    def translate(self, disp):
        super().translate(disp)
        self.update_points_normals()


class UniformPolygon(Polygon):
    def __init__(self, pos, vel, offsets, color=(0, 0, 0), width=0, density=1, angle=0, avel=0, momi=0, mass=0, **kwargs):

        self.pos = pos
        self.mass = mass
        self.vel = vel
        self.offsets = offsets
        self.color = color
        self.width = width
        self.density = density
        self.angle = angle
        self.avel = avel
        self.momi = momi

        A = 0
        totalMass = 0
        momi = 0
        R_Total = Vec2(0, 0)
        R = 0

        for i in range(len(offsets)):
            # area of the
            A = 1 / 2 * offsets[i] % offsets[i - 1]
            totalMass += A * density
            # mass of the triangle
            massTriangle = density * A
            # Moment of inertia
            momiT = massTriangle / 6 * (offsets[i].mag2() + offsets[i - 1].mag2() + offsets[i] @ offsets[i - 1])
            momi += momiT
            # Centroid of a triangle
            R = 1 / 3 * (offsets[i] + offsets[i - 1])
            # Centroid of entire shape (weighted average)
            R_Total += massTriangle * R
            # I_center = 1/3*(offsets[i] + offsets[i-1])
            # I_offcenter = I_center + massTriangle*R*R  # M = mass

        R_Total /= totalMass

        new_offsets = []
        for o in offsets:
            new_offsets.append(o - R_Total)
        if totalMass < 0:
            totalMass *= -1
            momi *= -1
        momi -= totalMass * R_Total.mag2()

        pos += R_Total

        for i in range(len(offsets)):
            offsets[i] -= R_Total

        super().__init__(offsets=offsets, mass=totalMass, pos=pos, vel=vel,  color=color, width=width, momi=momi, angle=angle, avel=avel)
        # angle=angle, avel=avel,     beween vel and color
