import pygame
from circle import Circle
from Vec2 import Vec2
from Wall import Wall
import math


def circle_circle(a, b):
    # Find overlap and normal
    r = a.pos - b.pos
    rmag = r.mag()
    d = (a.radius + b.radius) - rmag
    n = r.hat()
    return a, b, d, n


def circle_wall(circle, wall):
    # Find overlap and normal
    r = wall.pos - circle.pos
    n = wall.normal
    d = r @ n + circle.radius
    return circle, wall, d, n


def bounce(contact_data, restitution=0):
    if contact_data is not None:
        a, b, d, n = contact_data
        if d > 0:
            mia = 1 / a.mass
            mib = 1 / b.mass

            if mia == 0 and mib == 0:
                mia = 1
                mib = 1
            m = 1 / (mia + mib)

            s = m * d * n
            a.pos += s * mia
            b.pos -= s * mib

            v = a.vel - b.vel
            vn = v @ n
            if vn < 0:
                J = (-m * (1 + restitution) * vn) * n
                a.vel += J * mia
                b.vel -= J * mib
            return 1
        return 0


def hole_resolve(contact_data, list):
    a, b, d, n, = contact_data
    if d > 0:
        a.add_force(-n * 500)
    if d > 2*a.radius:
        # remove ball
        list.remove(a)


def contact2(a, b, resolve=bounce, **kwargs):
    if isinstance(a, Circle) and isinstance(b, Circle):
        return resolve(circle_circle(a, b), **kwargs)
    if isinstance(a, Circle) and isinstance(b, Wall):
        return resolve(circle_wall(a, b), **kwargs)
    if isinstance(a, Wall) and isinstance(b, Circle):
        return resolve(circle_wall(b, a), **kwargs)

