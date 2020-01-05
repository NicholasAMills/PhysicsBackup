from Vec2 import Vec2


class Particle:
    def __init__(self, mass=float('inf'), pos=Vec2(0, 0), vel=Vec2(0, 0), angle=0, torque=0, momi=float('inf'), avel=0):
        self.mass = mass
        self.avel = avel
        self.pos = pos.copy()  # or Vec2(pos)
        self.vel = Vec2(vel)
        self.force = Vec2(0, 0)
        self.angle = angle
        self.torque = torque
        self.momi = momi

    def update(self, dt):
        self.vel += self.force/self.mass * dt
        self.pos += self.vel * dt
        self.angle += self.avel * dt
        self.avel += (self.torque / self.momi) * dt

    def clear_force(self):
        self.force = Vec2(0, 0)

    def add_force(self, force):
        self.force += force

    def add_impulse(self, j, p):
        self.vel += j / self.mass
        s = p - self.pos
        self.avel += (s % j) / self.momi

    def translate(self, disp):
        self.pos = self.pos + disp
