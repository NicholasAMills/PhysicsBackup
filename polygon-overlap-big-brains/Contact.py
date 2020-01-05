import pygame
from circle import Circle
from Vec2 import Vec2
from Wall import Wall
import math
from Polygon import Polygon


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
        a, b, d, n, p = contact_data
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


def polygon_polygon(a, b):
    minOverlap = float('inf')
    maxOverlap = -float('inf')
    norm = Vec2(0, 0)

    # max overlap: d = (ra - rb) @ norm(a)
    for i in range(len(a.points)):
        # do something
        aPoint = a.points[i]
        aNorm = a.normals[i]
        maxOverlap = -float('inf')
        for j in range(len(b.points)):
            bPoint = b.points[j]
            curOverlap = (aPoint - bPoint) @ aNorm
            if curOverlap > maxOverlap:
                maxPoint = bPoint
                maxOverlap = curOverlap
        if maxOverlap < minOverlap:
            norm = aNorm
            minOverlap = maxOverlap
            minPoint = maxPoint
        if minOverlap <= 0:
            return None

    for i in range(len(b.points)):
        # do something
        bPoint = b.points[i]
        bNorm = b.normals[i]
        maxOverlap = -float('inf')
        for j in range(len(a.points)):
            aPoint = a.points[j]
            curOverlap = (bPoint - aPoint) @ bNorm
            if curOverlap > maxOverlap:
                maxPoint = aPoint
                maxOverlap = curOverlap
        if maxOverlap < minOverlap:
            norm = bNorm
            minOverlap = maxOverlap
            minPoint = maxPoint
        if minOverlap <= 0:
            return None

    # return minOverlap, minPoint, norm
    return a, b, minOverlap, norm, minPoint


def output(a):
    if a is not None:
        return a
    else:
        return None


def contact(a, b, resolve=bounce, **kwargs):
    if isinstance(a, Circle) and isinstance(b, Circle):
        return resolve(circle_circle(a, b), **kwargs)
    if isinstance(a, Circle) and isinstance(b, Wall):
        return resolve(circle_wall(a, b), **kwargs)
    if isinstance(a, Circle) and isinstance(b, Wall):
        return resolve(circle_wall(b, a), **kwargs)
    if isinstance(a, Polygon) and isinstance(b, Polygon):
        return resolve(polygon_polygon(a, b), **kwargs)


