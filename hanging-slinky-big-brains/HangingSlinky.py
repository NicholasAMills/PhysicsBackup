import pygame
import random
from Vec2 import Vec2
from circle import Circle
from Forces import Gravity
from Forces import Spring
from Forces import AirResistance
from Forces import RepulsiveForce
from Forces import Wind
import math

ball = Circle()
objects = []
bonds = []
masses = []
exploded_objects = []
d = 80

screen = pygame.display.set_mode(size=[800, 600])

for i in range(5):
    # radius = random.uniform(20, 40)
    radius = random.randint(30, 35)
    randomMass = random.randint(10, 13)
    randomColor = ([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
    if i is 0:
        ball = (Circle(radius=radius, color=randomColor, pos=Vec2(400, 50 + d * i), vel=Vec2(0, 0), mass=math.inf))
    else:
        ball = (Circle(radius=radius, color=randomColor, pos=Vec2(400, 50 + d * i), vel=Vec2(0, 0), mass=randomMass))

    objects.append(ball)
    masses.append(ball.mass)

def main():
    # Set up pygame and window
    pygame.init()
    forces = []
    # Set background color
    bg_color = [255, 255, 255]
    # Set the screen size
    screen.fill(bg_color)

    # Game Loops
    running = True
    # clock within pygame
    clock = pygame.time.Clock()
    # Set the fps of the game to 60
    fps = 60
    dt = 1 / fps

    drag = False
    objToDrag = 0

    # FORCES
    grav = Gravity(objects, Vec2(0, 1000))
    forces.append(grav)

    air = AirResistance(objects, 0.001)
    forces.append(air)

    w = 0
    wind = Wind(objects, 0.0001, Vec2(0, 0))
    print(wind)
    forces.append(wind)

    pair_list = []
    for i in range(len(objects) - 1):
        pair_list.append([objects[i], objects[i + 1]])

    print(pair_list)
    spring = Spring(pair_list, 1000, 60, 10)
    forces.append(spring)

    repulsive = RepulsiveForce(objects, 2000)
    forces.append(repulsive)

    print(masses)

    while running:
        for o in objects:
            o.clear_force()

        # Add Force
        for f in forces:
            f.apply()
        # Move objects
        for o in objects:
            o.update(dt)

        # Draw objects to screen
        screen.fill(bg_color)

        spring.draw(screen)

        for o in objects:
            o.draw(screen)

        # Shows changes to entire screen
        pygame.display.flip()

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        for o in objects:
            if o.pos.y > 2000:
                objects.pop(objects.index(o))

        # print(len(objects))

        # Event Loop
        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Checking if mouse is inside a circle
                for o in objects:
                    sqx = (x - o.pos.x) ** 2
                    sqy = (y - o.pos.y) ** 2
                    if math.sqrt(sqx + sqy) < o.radius:
                        drag = True
                        objToDrag = objects.index(o)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                drag = False
                for o in objects:
                    if objects.index(o) == objToDrag:
                        o.vel = Vec2(0, 0)
                        o.mass = masses[objects.index(o)]
                        # print(o.mass)
            elif e.type == pygame.MOUSEMOTION:
                if drag:
                    for o in objects:
                        if objects.index(o) == objToDrag:
                            o.vel = Vec2(0, 0)
                            o.mass = math.inf
                            o.pos.x = pygame.mouse.get_pos()[0]
                            o.pos.y = pygame.mouse.get_pos()[1]
                            # print(o.mass)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Checking if mouse is inside a circle
                for o in objects:
                    sqx = (x - o.pos.x) ** 2
                    sqy = (y - o.pos.y) ** 2
                    if math.sqrt(sqx + sqy) < o.radius:
                        for p in pair_list:
                            if pair_list.index(p) == objects.index(o):
                                pair_list.pop(pair_list.index(p))
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    r = Wind(objects, 0.0001, Vec2(1000, 0))
                    forces.append(r)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    forces.pop()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    l = Wind(objects, 0.0001, Vec2(-1000, 0))
                    forces.append(l)
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    forces.pop()

    # Shut down pygame
    pygame.quit()


# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
