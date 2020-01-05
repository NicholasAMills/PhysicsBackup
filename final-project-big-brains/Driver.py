import itertools
import pygame
from Vec2 import Vec2
from Contact import contact
from Contact import point_polygon
import math
from Wall import Wall
from Forces import Gravity
from Polygon import UniformPolygon
from Contact import output
from circle import Circle
import random
from Forces import Gravitation
from Forces import Thrust

masses = []
objects = []
passive_objects = []
rocket = []
miniRocket = []
miniRocket_difference = []
walls = []
thrust = []
thrustObjects = []
thrustObjectsFin = []
screen = pygame.display.set_mode(size=[1500, 800])
grav = Gravity(objects, Vec2(0, 10))
earth_radius = 6371000

def thrustDraw():
    radius = random.randint(1, 5)
    color = (random.randint(100, 255), 0, 0)

    thrustDown = (Circle(radius=radius, color=color, pos=Vec2(0, 0), vel=Vec2(0, 0), mass=1))
    return thrustDown

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

    blueTriangleCheck = True

    BLACK = [0, 0, 0]
    RED = [255, 0, 0]
    BLUE = [0, 0, 255]
    EXOSPHERE = [0, 0, 100]
    SKY = [0, 150, 255]
    YELLOW = [255, 255, 0]
    GREEN = [0, 255, 0]
    PURPLE = [255, 0, 255]

    # Declaring shapes
    # OFFSETS TO CREATE SHAPES
    rocket_tip_offset = [Vec2(0, -30), Vec2(-30, 0), Vec2(30, 0)]
    rocket_tip_offset.reverse()
    rocket_Body_Offsets = [Vec2(-20, -40), Vec2(-20, 40), Vec2(20, 40), Vec2(20, -40)]
    rocket_Body_Offsets.reverse()
    leftWing_Offsets = [Vec2(-30,0), Vec2(0,-30), Vec2()]
    leftWing_Offsets.reverse()
    rightWing_Offsets = [Vec2(30, 0), Vec2(0, -30), Vec2()]
    rightWing_Offsets.reverse()

    mini_rocket_tip_offset = [Vec2(0, -7.5), Vec2(-7.5, 0), Vec2(7.5, 0)]
    mini_rocket_tip_offset.reverse()
    mini_rocket_Body_Offsets = [Vec2(-5, -10), Vec2(-5, 10), Vec2(5, 10), Vec2(5, -10)]
    mini_rocket_Body_Offsets.reverse()
    mini_leftWing_Offsets = [Vec2(-7.5, 0), Vec2(0, -7.5), Vec2()]
    mini_leftWing_Offsets.reverse()
    mini_rightWing_Offsets = [Vec2(7.5, 0), Vec2(0, -7.5), Vec2()]
    mini_rightWing_Offsets.reverse()

    # PLACING ROCKET
    body_position = Vec2(750, 550)  # Change this value to move rocket. DO NOT TOUCH THE DIFFERENCES!!!
    tip_difference = Vec2(0, -41)
    leftWing_difference = Vec2(-21, 40)
    rightWingDifference = Vec2(21, 40)
    window_difference = Vec2(0, -10)

    # PLACING MINI ROCKET
    mini_body_position = Vec2(100, 610)  # Change this value to move rocket. DO NOT TOUCH THE DIFFERENCES!!!
    mini_tip_difference = Vec2(0, -10.25)
    mini_leftWing_difference = Vec2(-5.25, 10)
    mini_rightWingDifference = Vec2(5.25, 10)
    mini_window_difference = Vec2(0, -2.25)

    miniRocket_difference.append(mini_body_position)
    miniRocket_difference.append(mini_tip_difference)
    miniRocket_difference.append(mini_leftWing_difference)
    miniRocket_difference.append(mini_rightWing_Offsets)
    miniRocket_difference.append(mini_window_difference)


    rocket_tip = UniformPolygon(mass=30, pos=body_position + tip_difference, vel=Vec2(0, 0), offsets=rocket_tip_offset, color=BLACK,
                                width=0)
    rocketBody = UniformPolygon(mass=22200, pos=body_position, vel=Vec2(0, 0), offsets=rocket_Body_Offsets,
                                color=(200, 200, 200), width=0)
    leftWing = UniformPolygon(mass=10, pos=body_position + leftWing_difference, vel=Vec2(0, 0), offsets=leftWing_Offsets, color=BLACK,
                              width=0)
    rightWing = UniformPolygon(mass=10, pos=body_position + rightWingDifference, vel=Vec2(0, 0), offsets=rightWing_Offsets, color=BLACK,
                               width=0)
    window = Circle(10, BLACK, pos=body_position + window_difference)

    # Mini Rocket
    mini_rocket_tip = UniformPolygon(mass=0, pos=mini_body_position + mini_tip_difference, vel=Vec2(0, 0), offsets=mini_rocket_tip_offset,
                                color=BLACK,
                                width=0)
    mini_rocketBody = UniformPolygon(mass=0, pos=mini_body_position, vel=Vec2(0, 0), offsets=mini_rocket_Body_Offsets,
                                color=(200, 200, 200), width=0)
    mini_leftWing = UniformPolygon(mass=0, pos=mini_body_position + mini_leftWing_difference, vel=Vec2(0, 0),
                              offsets=mini_leftWing_Offsets, color=BLACK,
                              width=0)
    mini_rightWing = UniformPolygon(mass=0, pos=mini_body_position + mini_rightWingDifference, vel=Vec2(0, 0),
                               offsets=mini_rightWing_Offsets, color=BLACK,
                               width=0)
    mini_window = Circle(2.5, BLACK, pos=mini_body_position + mini_window_difference)

    # rocket.append(rocket_tip)
    rocket.append(rocketBody)
    # rocket.append(leftWing)
    # rocket.append(rightWing)
    rocket.append(window)

    # objects.append(rocket_tip)
    # objects.append(rocketBody)
    objects.append(leftWing)
    # objects.append(rightWing)

    miniRocket.append(mini_rocket_tip)
    miniRocket.append(mini_rocketBody)
    miniRocket.append(mini_leftWing)
    miniRocket.append(mini_rightWing)
    miniRocket.append(mini_window)

    groundWall = Wall(pos=Vec2(750, 590), normal=Vec2(0, -1), length=750, color=BLACK)
    objects.append(groundWall)
    walls.append(groundWall)

    font = pygame.font.SysFont('Calibri', 20, True, False)
    thrustText = font.render("THRUST", True, BLACK)
    fuelText = font.render("FUEL", True, BLACK)

    thrust = False
    thrustScale = 0
    fuelAmount = 200
    fuelRemaining = True
    miniRocket_start_loc = 0
    drawThrust = False
    leftMax = False
    rightMax = False
    isRotating = False

    distRemaining = 0

    # moonPosY = -384400000
    moonPosY = -500000
    moonRadius = 1737100
    moon = Circle(radius=moonRadius, color=(100, 100, 100), pos=Vec2(0, moonPosY), mass=float('inf'))
    passive_objects.append(moon)
    rocketRotate = False
    rotateAmount = 0

    earthMass = 5.972 * 10**24
    earth = Circle(radius=earth_radius, color=GREEN, pos=Vec2(750, earth_radius + 550), mass=earthMass)
    passive_objects.append(earth)

    for w in walls:
        passive_objects.append(w)

    gravitationArr = []
    # for r in rocket:
    #     gravitationArr.append(r)
    gravitationArr.append(rocketBody)
    gravitationArr.append(earth)
    G = 6.7 * 10**-11
    # G = 0.000000001
    # gravity
    grav = Gravitation(gravitationArr, G)
    forces.append(grav)

    rocketOffset = 0

    rocketThrust = Thrust(rocket, 1000000, 1000000, 1000000, 0, 10000000)

    while running:
        for g in gravitationArr:
            g.clear_force()

        rocketBody.pos = Vec2(750, 550)

        for o in objects:
            o.clear_force()

        for w in walls:
            w.update(dt)
            w.clear_force()
            w.draw(screen)

        # Add Force
        for f in forces:
            f.apply()

        # Draw objects to screen
        # Level 1: background is normal sky
        if distRemaining > (500000 - (500000/3)):
            screen.fill(SKY)
        # Level 2: background is dark, but not black yet
        elif distRemaining > 166666 and distRemaining < 333333:
            screen.fill(EXOSPHERE)
        # Level 3: background is black, like space
        elif distRemaining <= 166666:
            screen.fill(BLACK)
            # window.color = EXOSPHERE

        for t in thrustObjectsFin:
            if t.pos.y > rocketBody.pos.y + 150:
                thrustObjectsFin.pop(thrustObjectsFin.index(t))

        if drawThrust:
            if len(thrustObjects) < 100:
                thrustObjects.append(thrustDraw())
            for t in thrustObjects:
                t.pos = Vec2(rocketBody.pos.x + random.randint(-10, 10), rocketBody.pos.y + 40)
                t.vel = Vec2(random.randint(-50, 50), random.randint(200, 300))
                thrustObjectsFin.append(t)
                thrustObjects.pop(thrustObjects.index(t))

        for r in rocket:
            r.avel = rotateAmount

        distRemaining = math.sqrt((moon.pos.x - rocketBody.pos.x)**2 + (moon.pos.y - rocketBody.pos.y)**2)

        if fuelAmount > 0:
            pygame.draw.rect(screen, RED, (1279, 61, fuelAmount, 17), 0)
        else:
            fuelRemaining = False

        for p in passive_objects:
            if distRemaining > 500280:
                p.draw(screen)
            p.update(dt)

        if distRemaining < 5000:
            moon.draw(screen)

        # for o in objects:
        #     if o != rocketBody: # stops rocketBody from being drawn twice. Need objects and rocket because of turning
        #         o.update(dt)
        #         o.draw(screen)

        for t in thrustObjectsFin:
            t.update(dt)
            t.draw(screen)

        for r in rocket:
            r.update(dt)
            r.draw(screen)

        rocketOffset = rocketBody.pos - body_position

        for p in passive_objects:
            # p.vel = Vec2(0, thrustScale * 10)  #55.88)
            p.pos -= rocketOffset
        rocketBody.pos -= rocketOffset

        print(len(forces))
        if thrust and fuelRemaining:
            drawThrust = True
            forces.append(rocketThrust)

            fuelAmount -= (0.1 / 4)
            # mini_rocketBody.pos = Vec2(100, miniRocket_start_loc)

            # NEED OFFSETS CHANGED FOR MINIROCKET (ALL OFFSETS JUMP TO 100)
            for m in miniRocket:
                # for n in miniRocket_difference:
                m.pos += Vec2(0, miniRocket_start_loc)

            if thrustScale < 200:

                thrustScale += 1.3
                miniRocket_start_loc -= 0.0002
                pygame.draw.rect(screen, YELLOW, (1279, 21, thrustScale, 17), 0)
            elif thrustScale >= 200:

                miniRocket_start_loc -= 0.00035
                thrustScale = 200
                pygame.draw.rect(screen, YELLOW, (1279, 21, thrustScale, 17), 0)
        else:
            thrustScale = 0
            miniRocket_start_loc = 0
            drawThrust = False

        # if isRotating:
        #     if not rightMax:
        #         rotateAmount = -1
        #     else:
        #         rotateAmount = 0
        #     if not leftMax:
        #         rotateAmount = 1
        #     else:
        #         rotateAmount = 0

        # Creates Progress Slider on the side of the screen and adds it into a list to be drawn
        pygame.draw.line(screen, BLACK, Vec2(100, 40), Vec2(100, 700), 3)
        pygame.draw.line(screen, BLACK, Vec2(50, 220), Vec2(150, 220), 3)
        pygame.draw.line(screen, BLACK, Vec2(50, 440), Vec2(150, 440), 3)
        pygame.draw.circle(screen, (200, 200, 200), Vec2(100, 40), 20, 0)

        pygame.draw.circle(screen, BLUE, Vec2(100, 700), 80, 0)

        # Creates Thrust and Fuel Bars on top right of screen
        screen.blit(thrustText, [1200, 20])
        screen.blit(fuelText, [1200, 60])
        pygame.draw.rect(screen, BLACK, (1277, 20, 203, 20), 3)
        pygame.draw.rect(screen, BLACK, (1277, 60, 203, 20), 3)

        for m in miniRocket:
            m.update(dt)
            m.draw(screen)

        # checking collisions
        for a, b in itertools.combinations(objects, 2):
            contact(a, b, restitution=0)

        # Wait
        fps = 60
        clock.tick(fps) / 1000

        key = pygame.key.get_pressed()  # referencing key event
        # Event Loop

        contactResult = ()

        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    isRotating = True
                    if rocketBody.angle <= 0.45:
                        rightMax = False
                    else:
                        rightMax = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    isRotating = True
                    if rocketBody.angle >= -0.45:
                        leftMax = False
                    else:
                        leftMax = True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    isRotating = False

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    isRotating = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and fuelRemaining:
                    thrust = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    thrust = False

        pygame.display.flip()


    # Shut down pygame
    pygame.quit()


# Safe start
if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
