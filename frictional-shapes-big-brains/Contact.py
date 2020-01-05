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

def polygon_wall(a, b):
    # r = b.pos - a.pos
    # n = b.normal
    # d = r @ n + a.width
    minOverlap = float('inf')
    maxOverlap = -float('inf')
    norm = Vec2(0, 0)

    #for i in range(len(b.pos)):
        # do something
    bPoint = b.pos
    bNorm = b.normal
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

            ra = p - a.pos
            rb = p - b.pos

            v = (a.vel + a.avel * ~ra) - (b.vel + b.avel * ~rb)
            vn = v @ n
            if vn < 0:
                m = 1/(mia + mib + ((ra % n)**2 / a.momi) + ((rb % n)**2 / b.momi))
                j = (-m * (1 + restitution) * vn) * n
                a.add_impulse(j, p)
                b.add_impulse(-j, p)
            return 1
        return 0


def point_polygon(a, b):
    print("Hi")
    minOverlap = float('inf')
    maxOverlap = -float('inf')
    norm = Vec2(0, 0)
    penetrator = None
    penetrated = None

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
            penetrator = b
            penetrated = a

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
            penetrator = a
            penetrated = b
        if minOverlap <= 0:
            return None

    # return minOverlap, minPoint, norm
    return penetrator, penetrated, minOverlap, norm, minPoint


def polygon_polygon(a, b):
    minOverlap = float('inf')
    maxOverlap = -float('inf')
    norm = Vec2(0, 0)
    penetrator = None
    penetrated = None

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
            penetrator = b
            penetrated = a

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
            penetrator = a
            penetrated = b
        if minOverlap <= 0:
            return None

    # return minOverlap, minPoint, norm
    return penetrator, penetrated, minOverlap, norm, minPoint


def output(a):
    if a is not None:
        return a
    else:
        return None


def Static_friction(a, b, n, er):
    t = n.perp()
    # San2 = S @ a.normals **2
    # Sbn2 = S @ b.normals **2
    # Sat2 = S @ t **2
    # Sbt2 = S @ t **2
    # Mnn = 1/a.mass + 1/b.mass + San2/a.momi + Sbn2/b.momi
    # Mtt = 1/a.mass + 1/b.mass + Sat2/a.momi + Sbt2/b.momi
    # Mnt = (Sat*Sat)/a.momi + (Sbn*Sbt)/b.momi
    # dVn = -(1 + er) * vn
    # dVt = -2*vt
    # J = Jn*n+Jt*t




def contact(a, b, resolve=bounce, **kwargs):
    if isinstance(a, Circle) and isinstance(b, Circle):
        return resolve(circle_circle(a, b), **kwargs)
    if isinstance(a, Circle) and isinstance(b, Wall):
        return resolve(circle_wall(a, b), **kwargs)
    if isinstance(a, Circle) and isinstance(b, Wall):
        return resolve(circle_wall(b, a), **kwargs)
    if isinstance(a, Polygon) and isinstance(b, Polygon):
        return resolve(polygon_polygon(a, b), **kwargs)
    if isinstance(a, Polygon) and isinstance(b, Wall):
        return resolve(polygon_wall(a, b), **kwargs)
    if isinstance(a, Wall) and isinstance(b, Polygon):
        return resolve(polygon_wall(b, a), **kwargs)
