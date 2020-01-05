import math
import itertools
from Vec2 import Vec2
import pygame


# class Force:
class SingleForce:
    def __init__(self, list):
        self.list = list

    def force(self, o):
        return Vec2(0, 0)

    def apply(self):
        for o in self.list:
            o.add_force(self.force(o))

    def remove(self, o):
        self.list.remove(o)


class Bond:
    def __init__(self, list):
        self.list = list

    def apply(self):
        for pair in self.list:
            a, b = pair
            force = self.force(a, b)  # force on a from b
            a.add_force(force)
            b.add_force(-force)

    def remove(self, o):
        to_remove = []
        for pair in self.list:
            if pair[0] is o or pair[1] is o:
                to_remove.append(pair)
        for p in to_remove:
            self.list.remove(p)


class PairForces:
    def __init__(self, list):
        self.list = list

    # def force(self, o):
    def apply(self):
        for a, b in itertools.combinations(self.list, 2):
            force = self.force(a, b)  # force on a from b
            a.add_force(force)
            b.add_force(-force)


class Friction(SingleForce):
    def __init__(self, list):
        super().__init__(list)

    def force(self, o):
        return -o.vel.hat() * 100


class AttractiveForce(PairForces):
    def __init__(self, list):
        super().__init__(list)

    def force(self, a, b):
        e = 200 * a.radius * b.radius
        l = a.radius + b.radius
        r = a.pos - b.pos
        return e * ((l / r.mag()) ** 2 - 1) * (l / r.mag()) ** 2 * r.hat()


