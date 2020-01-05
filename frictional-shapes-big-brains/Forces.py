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


class Spring(Bond):
    def __init__(self, list, k, length, b, line_color=(0, 0, 0), line_width=2):
        super().__init__(list)
        self.k = k
        self.length = length
        self.b = b  # damping
        self.line_color = line_color
        self.line_width = line_width

    def force(self, a, b):
        r = a.pos - b.pos
        return -self.k * (r.mag() - self.length) * r.hat() - self.b * (a.vel - b.vel)@r.hat() * r.hat()

    def draw(self, screen):
        for pair in self.list:
            a, b = pair
            pygame.draw.line(screen, (0, 0, 0), a.pos.int(), b.pos.int(), self.line_width)

class Gravity(SingleForce):
    def __init__(self, list, g):
        super().__init__(list)
        self.g = g

    def force(self, o):
        if o.mass == math.inf:
            return Vec2(0, 0)
        return o.mass * self.g


class Gravitation(PairForces):
    def __init__(self, list, G):
        super().__init__(list)
        self.G = G

    def force(self, a, b):
        r = a.pos - b.pos
        return -self.G * a.mass * b.mass / r.mag2() * r.hat()


class Wind(SingleForce):
    def __init__(self, list, d=1, wind=Vec2()):
        super().__init__(list)
        self.d = d
        self.wind = wind
    def force(self, o):
        vel = o.vel - self.wind
        return -2 * self.d * o.radius * vel.mag() * vel


class AirResistance(SingleForce):
    def __init__(self, list, d):
        super().__init__(list)
        self.d = d

    def force(self, o):
        return -self.d * Vec2.mag2(o.vel) * o.vel.hat()


class StaticFriction(SingleForce):
    def __init__(self, list):
        super().__init__(list)

    def force(self, n, o, offsets, a, b):
        # vList = [][]
        # t = n.perp()
        #
        # Mnn = 1/a.mass + 1/b.mass + ((a.offsets * a.normal).mag2()/a.momi) + ((b.offsets*b.normal).mag2()/b.momi)

        '''
        1. Calculate for static fricion
            if |Jt|/|Jn| < mew_s:
                use J from static friction
            else:
        2. Calculate for kinetic friction
            mew = mew_k sgn(Jt) # Jt from before

        Kinetic friction:
        [dVn, dVt] = [Mtt -Mnt] [Jn]
                     [-M    1 ] [Jt]


        (if Vn > 0, return 0 # no collisions b/c moving away)
        if Static_friction is None:
            Static_friction = kinetic_friction
            if static_friction < kinetic_friction:
                static_friction = kinetic_friction
            if kinetic_friction is None:
                old stuff w/o friction
            else:
                new stuff with friction
        '''